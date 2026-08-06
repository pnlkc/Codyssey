/**
 * ConceptNote AI - Frontend Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const conceptForm = document.getElementById('concept-form');
  const keywordInput = document.getElementById('keyword-input');
  const levelSelect = document.getElementById('level-select');
  const btnGenerate = document.getElementById('btn-generate');
  const btnText = btnGenerate.querySelector('.btn-text');
  const spinner = document.getElementById('spinner');
  
  const resultContainer = document.getElementById('result-container');
  const resultKeyword = document.getElementById('result-keyword');
  const resultLevel = document.getElementById('result-level');
  const resultDefinition = document.getElementById('result-definition');
  const resultFeatures = document.getElementById('result-features');
  const resultAnalogy = document.getElementById('result-analogy');
  const resultExample = document.getElementById('result-example');
  const btnSaveNote = document.getElementById('btn-save-note');
  
  const errorMessage = document.getElementById('error-message');
  const errorText = document.getElementById('error-text');
  
  const savedNotesGrid = document.getElementById('saved-notes-grid');
  const emptyState = document.getElementById('empty-state');
  const savedCount = document.getElementById('saved-count');
  const btnClearNotes = document.getElementById('btn-clear-notes');
  const toastContainer = document.getElementById('toast-container');

  // Active Current Generated Note Object
  let currentGeneratedNote = null;

  // Initialize Saved Notes from LocalStorage
  loadSavedNotes();

  // Form Submit Event Handler
  conceptForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const keyword = keywordInput.value.trim();
    const level = levelSelect.value;

    // 1. Validation check for empty input
    if (!keyword) {
      showToast('⚠️ 학습할 키워드를 입력해 주세요.');
      keywordInput.focus();
      return;
    }

    // Reset State
    hideError();
    setLoadingState(true);

    try {
      // 2. Fetch API Call to Vercel Serverless Function (/api/explain)
      const response = await fetch('/api/explain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ keyword, level })
      });

      // 3. API Error handling (4xx / 5xx)
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `서버 응답 오류 (HTTP ${response.status})`);
      }

      const data = await response.json();
      
      if (!data || !data.definition) {
        throw new Error('올바르지 않은 응답 포맷입니다.');
      }

      // Store current note data
      currentGeneratedNote = {
        id: Date.now(),
        keyword: data.keyword || keyword,
        level: data.level || level,
        definition: data.definition,
        features: data.features || [],
        analogy: data.analogy || '',
        example: data.example || '',
        createdAt: new Date().toLocaleDateString('ko-KR')
      };

      // Render Result Card
      renderResultCard(currentGeneratedNote);
      showToast('✨ AI 개념 노트 생성이 완료되었습니다!');

    } catch (err) {
      console.error('Fetch Error:', err);
      showError(err.message || 'AI 개념 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.');
      showToast('❌ 생성 실패: ' + err.message);
    } finally {
      setLoadingState(false);
    }
  });

  // Render Generated Result Card
  function renderResultCard(note) {
    resultKeyword.textContent = note.keyword;
    resultLevel.textContent = note.level;
    resultDefinition.textContent = note.definition;
    
    // Features List
    resultFeatures.innerHTML = '';
    if (Array.isArray(note.features) && note.features.length > 0) {
      note.features.forEach(feat => {
        const li = document.createElement('li');
        li.textContent = feat;
        resultFeatures.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.textContent = '핵심 특징이 정리되었습니다.';
      resultFeatures.appendChild(li);
    }

    resultAnalogy.textContent = note.analogy || '추가 비유 설명이 제공되지 않았습니다.';
    resultExample.textContent = note.example || '// 관련 예시 코드 또는 활용법이 여기에 표시됩니다.';

    resultContainer.classList.remove('hidden');
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Save Note Event
  btnSaveNote.addEventListener('click', () => {
    if (!currentGeneratedNote) return;

    let notes = getNotesFromStorage();
    // Duplicate check
    const exists = notes.some(n => n.keyword.toLowerCase() === currentGeneratedNote.keyword.toLowerCase());
    if (exists) {
      showToast('ℹ️ 이미 메모장에 저장된 키워드입니다.');
      return;
    }

    notes.unshift(currentGeneratedNote);
    saveNotesToStorage(notes);
    loadSavedNotes();
    showToast('📌 내 메모장에 안전하게 저장되었습니다!');
  });

  // Clear All Notes Event
  btnClearNotes.addEventListener('click', () => {
    const notes = getNotesFromStorage();
    if (notes.length === 0) {
      showToast('ℹ️ 삭제할 저장 노드가 없습니다.');
      return;
    }

    if (confirm('저장된 모든 개념 노트를 삭제하시겠습니까?')) {
      localStorage.removeItem('concept_notes');
      loadSavedNotes();
      showToast('🗑️ 저장된 메모가 모두 삭제되었습니다.');
    }
  });

  // LocalStorage Helper Functions
  function getNotesFromStorage() {
    try {
      const data = localStorage.getItem('concept_notes');
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  }

  function saveNotesToStorage(notes) {
    localStorage.setItem('concept_notes', JSON.stringify(notes));
  }

  function loadSavedNotes() {
    const notes = getNotesFromStorage();
    savedCount.textContent = notes.length;

    // Clear Grid
    savedNotesGrid.innerHTML = '';

    if (notes.length === 0) {
      savedNotesGrid.appendChild(emptyState);
      emptyState.classList.remove('hidden');
      return;
    }

    emptyState.classList.add('hidden');

    notes.forEach(note => {
      const card = document.createElement('div');
      card.className = 'note-card';
      card.innerHTML = `
        <div>
          <div class="concept-badge-group" style="margin-bottom: 10px;">
            <span class="badge badge-primary">${escapeHtml(note.keyword)}</span>
            <span class="badge badge-secondary">${escapeHtml(note.level)}</span>
          </div>
          <h4 class="note-card-title">${escapeHtml(note.keyword)}</h4>
          <p class="note-card-desc">${escapeHtml(note.definition)}</p>
        </div>
        <div class="note-card-footer">
          <span>📅 ${note.createdAt}</span>
          <button class="btn btn-danger-outline btn-sm btn-delete-note" data-id="${note.id}">삭제</button>
        </div>
      `;

      // Card Click Event (Open Detail Modal)
      card.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-delete-note')) return;
        openNoteModal(note);
      });

      // Single Delete Click
      const btnDelete = card.querySelector('.btn-delete-note');
      btnDelete.addEventListener('click', (e) => {
        e.stopPropagation();
        deleteNote(note.id);
      });

      savedNotesGrid.appendChild(card);
    });
  }

  // Note Detail Modal Logic
  const noteModal = document.getElementById('note-modal');
  const modalClose = document.getElementById('modal-close');
  const modalKeyword = document.getElementById('modal-keyword');
  const modalLevel = document.getElementById('modal-level');
  const modalDefinition = document.getElementById('modal-definition');
  const modalFeatures = document.getElementById('modal-features');
  const modalAnalogy = document.getElementById('modal-analogy');
  const modalExample = document.getElementById('modal-example');

  function openNoteModal(note) {
    modalKeyword.textContent = note.keyword;
    modalLevel.textContent = note.level;
    modalDefinition.textContent = note.definition;
    
    modalFeatures.innerHTML = '';
    if (Array.isArray(note.features) && note.features.length > 0) {
      note.features.forEach(feat => {
        const li = document.createElement('li');
        li.textContent = feat;
        modalFeatures.appendChild(li);
      });
    }

    modalAnalogy.textContent = note.analogy || '추가 비유 설명이 제공되지 않았습니다.';
    modalExample.textContent = note.example || '// 실무 예시가 제공되지 않았습니다.';

    noteModal.classList.remove('hidden');
  }

  modalClose.addEventListener('click', () => {
    noteModal.classList.add('hidden');
  });

  noteModal.addEventListener('click', (e) => {
    if (e.target === noteModal) {
      noteModal.classList.add('hidden');
    }
  });

  function deleteNote(id) {
    let notes = getNotesFromStorage();
    notes = notes.filter(n => n.id !== id);
    saveNotesToStorage(notes);
    loadSavedNotes();
    showToast('🗑️ 노드가 삭제되었습니다.');
  }

  // UI State Utility
  function setLoadingState(isLoading) {
    if (isLoading) {
      btnGenerate.disabled = true;
      spinner.classList.remove('hidden');
      btnText.textContent = 'AI 분석 및 작성 중...';
    } else {
      btnGenerate.disabled = false;
      spinner.classList.add('hidden');
      btnText.textContent = '✨ AI 개념 노트 생성하기';
    }
  }

  function showError(msg) {
    errorText.textContent = msg;
    errorMessage.classList.remove('hidden');
  }

  function hideError() {
    errorMessage.classList.add('hidden');
  }

  function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3000);
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
});
