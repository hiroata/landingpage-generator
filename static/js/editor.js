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
      
      // AIリクエスト用データ
      const sectionType = document.getElementById('section-type').value;
      const contextData = {
        business_type: document.getElementById('business_type').value || 'product',
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
    
    // 通知を表示
    document.body.appendChild(notification);
    
    // 閉じるボタンのイベント設定
    notification.querySelector('.notification-close').addEventListener('click', function() {
      notification.remove();
    });
    
    // 自動的に閉じる
    setTimeout(() => {
      notification.classList.add('notification-hiding');
      setTimeout(() => notification.remove(), 500);
    }, 5000);
  }
  
  // 生成されたコンテンツをフォームに適用
  function applyGeneratedContent(content, sectionType) {
    try {
      // セクションタイプに応じた解析と適用
      switch (sectionType) {
        case 'header':
          parseHeaderContent(content);
          break;
        case 'features':
          parseFeaturesContent(content);
          break;
        case 'about':
          parseAboutContent(content);
          break;
        case 'cta':
          parseCTAContent(content);
          break;
        case 'pricing':
          parsePricingContent(content);
          break;
        default:
          // 解析ロジックがない場合はモーダルで表示
          showContentModal(content);
      }
    } catch (error) {
      console.error('Content parsing error:', error);
      showNotification('コンテンツの解析に失敗しました', 'error');
      showContentModal(content);
    }
  }
  
  // 初期化
  document.addEventListener('DOMContentLoaded', function() {
    // 機能初期化
    initSectionDragDrop();
    initAIContentGeneration();
    
    // セクション保存ボタン
    const saveButton = document.getElementById('save-section');
    if (saveButton) {
      saveButton.addEventListener('click', function() {
        // 保存処理（実装は省略）
      });
    }
  });