/**
 * ランディングページ生成ツール - プレビュー機能
 */

// レスポンシブプレビュー設定
function initResponsivePreview() {
    const previewContainer = document.getElementById('preview-container');
    const viewportSizeDisplay = document.querySelector('.viewport-size');
    const deviceButtons = document.querySelectorAll('.device-button');
    
    if (!previewContainer || !viewportSizeDisplay || !deviceButtons.length) return;
    
    deviceButtons.forEach(button => {
      button.addEventListener('click', function() {
        // アクティブクラスを切り替え
        deviceButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        
        // コンテナの幅を設定
        const width = this.getAttribute('data-width');
        previewContainer.style.maxWidth = width;
        
        // 表示サイズを更新
        viewportSizeDisplay.textContent = width;
      });
    });
  }
  
  // セクション間のスクロールリンク
  function initSectionNavigation() {
    const sectionLinks = document.querySelectorAll('.section-nav-link');
    
    if (!sectionLinks.length) return;
    
    sectionLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        
        if (targetSection) {
          // スムーズスクロール
          targetSection.scrollIntoView({
            behavior: 'smooth'
          });
          
          // アクティブクラスを更新
          sectionLinks.forEach(link => link.classList.remove('active'));
          this.classList.add('active');
        }
      });
    });
  }
  
  // プレビュー印刷機能
  function initPrintPreview() {
    const printButton = document.getElementById('print-preview');
    
    if (!printButton) return;
    
    printButton.addEventListener('click', function() {
      // ツールバーを一時的に非表示
      const toolbar = document.querySelector('.preview-toolbar');
      const editButtons = document.querySelectorAll('.section-edit-button');
      
      if (toolbar) toolbar.style.display = 'none';
      editButtons.forEach(button => button.style.display = 'none');
      
      // 印刷
      window.print();
      
      // 表示を元に戻す
      setTimeout(() => {
        if (toolbar) toolbar.style.display = 'flex';
        editButtons.forEach(button => button.style.display = 'block');
      }, 1000);
    });
  }
  
  // ハイライトモード（セクション境界を表示）
  function initHighlightMode() {
    const highlightButton = document.getElementById('highlight-sections');
    const sectionPreviews = document.querySelectorAll('.section-preview');
    
    if (!highlightButton || !sectionPreviews.length) return;
    
    highlightButton.addEventListener('click', function() {
      const isActive = this.classList.toggle('active');
      
      sectionPreviews.forEach(section => {
        if (isActive) {
          section.classList.add('highlight-section');
        } else {
          section.classList.remove('highlight-section');
        }
      });
    });
  }
  
  // 初期化
  document.addEventListener('DOMContentLoaded', function() {
    // プレビュー機能初期化
    initResponsivePreview();
    initSectionNavigation();
    initPrintPreview();
    initHighlightMode();
  });