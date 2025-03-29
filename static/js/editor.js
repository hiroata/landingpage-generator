/**
 * ランディングページ生成ツール - エディタ機能
 */

// セクションドラッグ&ドロップ機能
function initSectionDragDrop() {
    const sectionContainer = document.querySelector('.section-list');
    if (!sectionContainer) return;
  
    new Sortable(sectionContainer, {
      animation: 150,
      handle: '.drag-handle',
      ghostClass: 'section-item-ghost',
      onEnd: function(evt) {
        // セクション順序変更後の処理
        const sectionIds = Array.from(document.querySelectorAll('.section-item'))
          .map(item => item.getAttribute('data-section-id'));
        
        // サーバーに順序変更を通知
        const projectId = document.getElementById('project-id').value;
        
        fetch(`/editor/reorder-sections/${projectId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ section_ids: sectionIds })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showNotification('セクションの順序を変更しました', 'success');
          } else {
            showNotification('順序の保存に失敗しました', 'error');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          showNotification('エラーが発生しました', 'error');
        });
      }
    });
  }
  
  // AIによるコンテンツ生成
  function initAIContentGeneration() {
    const generateButton = document.getElementById('ai-generate');
    if (!generateButton) return;
    
    generateButton.addEventListener('click', function() {
      // 現在編集中のセクション
      const currentSectionId = document.querySelector('.section-item.active')?.getAttribute('data-section-id');
      if (!currentSectionId) {
        showNotification('セクションを選択してください', 'warning');
        return;
      }
      
      // 必須入力チェック
      const businessName = document.getElementById('business_name').value;
      const industry = document.getElementById('industry').value;
      const targetAudience = document.getElementById('target_audience').value;
      const keyFeatures = document.getElementById('key_features').value;
      
      if (!businessName || !industry || !targetAudience || !keyFeatures) {
        showNotification('必須項目を入力してください', 'warning');
        return;
      }
      
      // ローディング表示
      generateButton.classList.add('loading');
      
      // 現在選択されているセクションのタイプを取得
      // 現在アクティブなセクションから直接タイプを取得する方法に変更
      const activeSection = document.querySelector('.section-item.active');
      const sectionType = activeSection ? activeSection.querySelector('.text-muted').textContent : 'header';
      
      // AIリクエスト用データ
      const contextData = {
        business_type: document.getElementById('business_type')?.value || 'product',
        business_name: businessName,
        industry: industry,
        target_audience: targetAudience,
        key_features: keyFeatures,
        tone: document.getElementById('tone').value,
        keywords: document.getElementById('keywords').value
      };
      
      // AI生成リクエスト
      fetch('/editor/generate-content', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section_type: sectionType,
          context: contextData
        })
      })
      .then(response => response.json())
      .then(data => {
        // ローディング終了
        generateButton.classList.remove('loading');
        
        if (data.success) {
          // 生成コンテンツのパースと適用
          applyGeneratedContent(data.content, sectionType);
          showNotification('コンテンツが生成されました', 'success');
        } else {
          showNotification('生成に失敗しました: ' + data.message, 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        generateButton.classList.remove('loading');
        showNotification('エラーが発生しました', 'error');
      });
    });
  }
  
  // 通知表示
  function showNotification(message, type = 'info') {
    // 既存の通知を削除
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
      existingNotification.remove();
    }
    
    // 新しい通知要素を作成
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
      </div>
      <button class="notification-close">&times;</button>
    `;
    
    // スタイルの追加
    notification.style.position = 'fixed';
    notification.style.bottom = '20px';
    notification.style.right = '20px';
    notification.style.backgroundColor = type === 'success' ? '#d4edda' : 
                                       type === 'error' ? '#f8d7da' : 
                                       type === 'warning' ? '#fff3cd' : '#d1ecf1';
    notification.style.color = type === 'success' ? '#155724' : 
                             type === 'error' ? '#721c24' : 
                             type === 'warning' ? '#856404' : '#0c5460';
    notification.style.border = '1px solid';
    notification.style.borderColor = type === 'success' ? '#c3e6cb' : 
                                   type === 'error' ? '#f5c6cb' : 
                                   type === 'warning' ? '#ffeeba' : '#bee5eb';
    notification.style.borderRadius = '4px';
    notification.style.padding = '15px';
    notification.style.maxWidth = '350px';
    notification.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
    notification.style.zIndex = '9999';
    
    // 通知を表示
    document.body.appendChild(notification);
    
    // 閉じるボタンのイベント設定
    notification.querySelector('.notification-close').addEventListener('click', function() {
      notification.remove();
    });
    
    // 自動的に閉じる
    setTimeout(() => {
      if (document.body.contains(notification)) {
        notification.style.opacity = '0';
        notification.style.transition = 'opacity 0.5s';
        setTimeout(() => notification.remove(), 500);
      }
    }, 5000);
  }
  
  // 生成されたコンテンツをフォームに適用
  function applyGeneratedContent(content, sectionType) {
    // 簡易的なアラートでコンテンツを表示する方法に変更
    try {
      // セクションタイプに応じた簡易解析
      if (sectionType === 'header' || sectionType.toLowerCase() === 'header') {
        // 簡易的にヘッダーセクションの内容を解析
        let headline = '', subheadline = '', cta_text = '';
        
        // 行単位で分割
        const lines = content.split('\n').filter(line => line.trim() !== '');
        
        // 1行目を見出しとして扱う
        if (lines.length > 0) {
          headline = lines[0].replace(/^[#\s]*/, '').trim();
          
          // 見出しフィールドに適用
          const headlineField = document.getElementById('headline');
          if (headlineField) headlineField.value = headline;
        }
        
        // 2行目があればサブ見出しとして扱う
        if (lines.length > 1) {
          subheadline = lines[1].trim();
          
          // サブ見出しフィールドに適用
          const subheadlineField = document.getElementById('subheadline');
          if (subheadlineField) subheadlineField.value = subheadline;
        }
        
        // 3行目以降にCTAテキストがあれば適用
        for (let i = 2; i < lines.length; i++) {
          if (lines[i].includes('ボタン') || lines[i].includes('今すぐ') || lines[i].includes('申し込む')) {
            cta_text = lines[i].replace(/^[*\-\s]*/, '').trim();
            
            // CTAテキストフィールドに適用
            const ctaTextField = document.getElementById('cta_text');
            if (ctaTextField) ctaTextField.value = cta_text;
            break;
          }
        }
      } else {
        // その他のセクションタイプはアラートでコンテンツを表示
        alert('生成されたコンテンツをフォームに適用してください:\n\n' + content);
      }
    } catch (error) {
      console.error('Content parsing error:', error);
      alert('生成されたコンテンツをご確認ください:\n\n' + content);
    }
  }
  
  // 初期化
  document.addEventListener('DOMContentLoaded', function() {
    // 機能初期化
    initAIContentGeneration();
    
    // Sortableライブラリが読み込まれている場合のみドラッグ&ドロップ初期化
    if (typeof Sortable !== 'undefined') {
      initSectionDragDrop();
    }
    
    // セクション保存ボタン
    const saveButton = document.getElementById('save-section');
    if (saveButton) {
      saveButton.addEventListener('click', function() {
        // 現在選択中のセクションがなければ何もしない
        const currentSection = document.querySelector('.section-item.active');
        if (!currentSection) {
          showNotification('セクションを選択してください', 'warning');
          return;
        }
        
        // プロジェクトID取得（URL等から取得する必要がある）
        const projectId = window.location.pathname.split('/').pop();
        const sectionId = currentSection.getAttribute('data-section-id');
        
        // セクションデータ収集の実装は既存コードを利用
        
        showNotification('セクションの保存処理を実行します', 'info');
      });
    }
  });