// ════════════════════════════════════════════════════════════
//   SYSTEM STATE
// ════════════════════════════════════════════════════════════
let currentMode = 'checklist';
let selectedPet = 'kucing';
let selectedSymptoms = new Set();
let chatbotPet = '';
let chatbotSymptoms = new Set();
let lastBotResponse = '';

// ════════════════════════════════════════════════════════════
//   INITIALIZATION
// ════════════════════════════════════════════════════════════
document.addEventListener("DOMContentLoaded", () => {
  buildChecklistGrids();
  clearChecklist();
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 30);
    });
  }
  document.getElementById('chat-send-btn').addEventListener('click', handleChatInput);
  document.getElementById('chat-input-field').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleChatInput();
  });
  hideChatInput();
});

function toggleNav() {
  const links = document.getElementById('nav-links');
  if (links) links.classList.toggle('open');
}

document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    const links = document.getElementById('nav-links');
    if (links) links.classList.remove('open');
  });
});

// ════════════════════════════════════════════════════════════
//   MODE SWITCHER
// ════════════════════════════════════════════════════════════
function switchMode(mode) {
  currentMode = mode;
  document.getElementById('tab-checklist').classList.toggle('active', mode === 'checklist');
  document.getElementById('tab-chatbot').classList.toggle('active', mode === 'chatbot');
  document.getElementById('panel-checklist').style.display = mode === 'checklist' ? 'block' : 'none';
  document.getElementById('panel-chatbot').style.display = mode === 'chatbot' ? 'block' : 'none';
  if (mode === 'chatbot') {
    restartChatBot();
  } else {
    clearChecklist();
  }
}

// ════════════════════════════════════════════════════════════
//   CHECKLIST MODE
// ════════════════════════════════════════════════════════════
function buildChecklistGrids() {
  renderSymptomGroup('container-semua-gejala', ALL_GEJALA_IDS);
}

function renderSymptomGroup(elementId, ids) {
  const container = document.getElementById(elementId);
  container.innerHTML = '';
  ids.forEach(id => {
    const item = document.createElement('div');
    item.className = 'gejala-card-item';
    item.id = `gc-${id}`;
    item.onclick = () => toggleChecklistSymptom(id);
    item.innerHTML = `
      <div class="checkbox-mock"></div>
      <div class="gejala-info">
        <span class="gejala-tag-code">${id}</span>
        <span class="gejala-label-text">${GEJALA[id]}</span>
      </div>
    `;
    container.appendChild(item);
  });
}

function toggleChecklistSymptom(id) {
  if (selectedSymptoms.has(id)) {
    selectedSymptoms.delete(id);
    document.getElementById(`gc-${id}`).classList.remove('checked');
  } else {
    selectedSymptoms.add(id);
    document.getElementById(`gc-${id}`).classList.add('checked');
  }
  const count = selectedSymptoms.size;
  document.getElementById('badge-counter').textContent = count;
  if (count > 0) {
    triggerBackendDiagnosis([...selectedSymptoms], selectedPet);
  } else {
    hideDiagnosis();
  }
}

function setPet(pet) {
  selectedPet = pet;
  document.getElementById('btn-pet-kucing').classList.toggle('selected', pet === 'kucing');
  document.getElementById('btn-pet-anjing').classList.toggle('selected', pet === 'anjing');
  if (selectedSymptoms.size > 0) {
    triggerBackendDiagnosis([...selectedSymptoms], selectedPet);
  }
}

function clearChecklist() {
  selectedSymptoms.clear();
  document.querySelectorAll('.gejala-card-item').forEach(el => el.classList.remove('checked'));
  document.getElementById('badge-counter').textContent = '0';
  setPet('kucing');
  hideDiagnosis();
}

// ════════════════════════════════════════════════════════════
//   FREE-CHAT DIAGNOSA ENGINE
// ════════════════════════════════════════════════════════════
const KEYWORD_MAP = [
  { keywords: ['demam', 'panas', 'suhu'], gid: 'G01' },
  { keywords: ['nafsu makan', 'tidak mau makan', 'susah makan', 'makan berkurang'], gid: 'G02' },
  { keywords: ['lemas', 'lemah', 'lesu', 'lunglai', 'tidak aktif'], gid: 'G03' },
  { keywords: ['perilaku', 'aneh', 'berubah', 'beda', 'tidak biasa'], gid: 'G04' },
  { keywords: ['mata merah', 'belekan', 'mata berair', 'konjungtivitis', 'mara merah'], gid: 'G05' },
  { keywords: ['penglihatan', 'kabur', 'buta', 'mata kabur', 'tidak melihat'], gid: 'G06' },
  { keywords: ['kejang', 'tremor', 'gemetar', 'kejang-kejang', 'kaku'], gid: 'G07' },
  { keywords: ['diare', 'muntah', 'mencret', 'berak', 'muntah-muntah'], gid: 'G08' },
  { keywords: ['sesak', 'napas berat', 'megap', 'susah napas', 'ngos-ngosan'], gid: 'G09' },
  { keywords: ['bengkak', 'kelenjar', 'getah bening', 'benjolan'], gid: 'G10' },
  { keywords: ['berat badan', 'kurus', 'turun', 'badan turun', 'kurus kering'], gid: 'G11' },
  { keywords: ['kuning', 'icterus', 'kekuningan', 'mata kuning'], gid: 'G12' },
  { keywords: ['saraf', 'jalan tidak seimbang', 'berputar', 'muter', 'linglung'], gid: 'G13' },
  { keywords: ['kotoran bau', 'feses bau', 'bau menyengat', 'berak bau'], gid: 'G14' },
  { keywords: ['agresif', 'galak', 'menyerang', 'menerkam', 'marah'], gid: 'G15' },
  { keywords: ['takut air', 'takut cahaya', 'hydrophobia', 'photophobia', 'takut minum'], gid: 'G16' },
  { keywords: ['air liur', 'berbusa', 'ngiler', 'liur', 'drool', 'busa'], gid: 'G17' },
  { keywords: ['rahang', 'sulit menelan', 'lumpuh rahang', 'rahang kaku', 'ngiler terus'], gid: 'G18' },
  { keywords: ['menggigit', 'mencakar', 'gigit', 'cakar', 'serang'], gid: 'G19' },
  { keywords: ['suara berubah', 'gonggong', 'meong', 'suara aneh', 'gonggongan'], gid: 'G20' },
  { keywords: ['bersembunyi', 'gelap', 'sembunyi', 'tempat gelap', 'menyendiri'], gid: 'G21' },
  { keywords: ['lumpuh', 'kaki', 'tungkai', 'gak bisa jalan', 'tidak bisa berdiri'], gid: 'G22' },
  { keywords: ['bingung', 'disorientasi', 'pusing', 'linglung', 'bizarre'], gid: 'G23' },
  { keywords: ['gigitan', 'vaksin', 'luka gigit', 'hewan liar', 'gigitan hewan'], gid: 'G24' },
];

function restartChatBot() {
  chatbotPet = '';
  chatbotSymptoms.clear();
  lastBotResponse = '';
  document.getElementById('chat-scroller').innerHTML = '';
  document.getElementById('bar-progress-fill').style.width = '0%';
  document.getElementById('label-chat-step').textContent = 'Free Chat';
  hideDiagnosis();
  showChatInput();
  setTimeout(() => {
    addBotMessage('Halo! Saya <strong>VetExpert</strong>, asisten diagnosa kesehatan hewan.');
    setTimeout(() => {
      addBotMessage('Ceritakan kondisi hewan Anda di sini.<br>Contoh: <i>"Anjing saya demam dan agresif"</i><br>atau <i>"Kucing lemas, mata merah"</i>');
    }, 600);
  }, 300);
}

function parseUserMessage(text) {
  const lower = text.toLowerCase();
  if (/\b(kucing|cat)\b/.test(lower)) {
    if (chatbotPet !== 'kucing') { chatbotPet = 'kucing'; return 'hewan'; }
  } else if (/\b(anjing|dog|asu)\b/.test(lower)) {
    if (chatbotPet !== 'anjing') { chatbotPet = 'anjing'; return 'hewan'; }
  }
  let found = false;
  for (const item of KEYWORD_MAP) {
    for (const keyword of item.keywords) {
      if (lower.includes(keyword)) {
        if (!chatbotSymptoms.has(item.gid)) { chatbotSymptoms.add(item.gid); found = true; }
        break;
      }
    }
  }
  if (found) return 'gejala';
  return 'unknown';
}

function generateChatbotResponse() {
  if (!chatbotPet) {
    return 'Silakan sebutkan jenis hewan Anda. Contoh: <b>Kucing</b> atau <b>Anjing</b>';
  }
  if (chatbotSymptoms.size === 0) {
    return 'Gejala tidak dikenali. Coba deskripsikan dengan kata lain. Misal: <i>"demam, lemas, mata merah"</i>';
  }
  triggerBackendDiagnosis([...chatbotSymptoms], chatbotPet);
  const daftar = [...chatbotSymptoms].map(gid => `• <b>${gid}</b>: ${GEJALA[gid]}`).join('<br>');
  let response = `${chatbotSymptoms.length} gejala terdeteksi:<br>${daftar}<br><br>`;
  response += '<b>Hasil Diagnosa</b> (lihat panel kanan)<br>';
  response += '<i>Ada gejala lain? Ceritakan saja...</i>';
  return response;
}

function handleChatInput() {
  const field = document.getElementById('chat-input-field');
  const text = field.value.trim();
  if (!text) return;
  field.value = '';
  addUserMessage(text);
  const result = parseUserMessage(text);
  if (result === 'unknown') {
    addBotMessage(generateChatbotResponse());
  } else {
    setTimeout(() => { addBotMessage(generateChatbotResponse()); }, 300);
  }
}

function showChatInput() {
  const inputArea = document.getElementById('chat-input-area');
  inputArea.style.display = 'flex';
  const field = document.getElementById('chat-input-field');
  field.value = '';
  setTimeout(() => field.focus(), 100);
}

function hideChatInput() {
  document.getElementById('chat-input-area').style.display = 'none';
}

function addBotMessage(html) {
  const chatScroll = document.getElementById('chat-scroller');
  const msg = document.createElement('div');
  msg.className = 'chat-msg bot';
  msg.innerHTML = `<div class="chat-msg-bubble">${html}</div><span class="chat-msg-time">${getCurrentTime()} · Asisten</span>`;
  chatScroll.appendChild(msg);
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

function addUserMessage(text) {
  const chatScroll = document.getElementById('chat-scroller');
  const msg = document.createElement('div');
  msg.className = 'chat-msg user';
  msg.innerHTML = `<div class="chat-msg-bubble">${text}</div><span class="chat-msg-time">${getCurrentTime()} · Anda</span>`;
  chatScroll.appendChild(msg);
  chatScroll.scrollTop = chatScroll.scrollHeight;
}

function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
}

// ════════════════════════════════════════════════════════════
//   DIAGNOSTIC BACKEND CONNECTOR
// ════════════════════════════════════════════════════════════
async function triggerBackendDiagnosis(symptomsArray, petType) {
  showLoading(true);
  document.getElementById('realtime-status-pill').textContent = 'Memproses...';
  document.getElementById('realtime-status-pill').style.background = 'var(--primary-light)';
  document.getElementById('realtime-status-pill').style.color = 'var(--primary)';
  try {
    const response = await fetch('/diagnosa', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gejala: symptomsArray, hewan: petType })
    });
    if (!response.ok) throw new Error("Terjadi kesalahan koneksi server.");
    const data = await response.json();
    renderDiagnosticResults(data);
  } catch (error) {
    console.error(error);
    document.getElementById('txt-summary-title').textContent = "Terjadi Kesalahan";
  } finally {
    showLoading(false);
    document.getElementById('realtime-status-pill').textContent = 'Aktif';
    document.getElementById('realtime-status-pill').style.background = 'var(--neutral-100)';
    document.getElementById('realtime-status-pill').style.color = 'var(--text-muted)';
  }
}

function renderDiagnosticResults(data) {
  const emptyState = document.getElementById('panel-empty-state');
  const resultsOutput = document.getElementById('panel-results-output');
  const cardsContainer = document.getElementById('container-disease-cards');
  emptyState.style.display = 'none';
  resultsOutput.style.display = 'flex';
  const petLabel = data.hewan === 'kucing' ? 'Kucing' : 'Anjing';
  if (!data.ada_diagnosa) {
    document.getElementById('txt-summary-title').textContent = "Tidak Ada Penyakit Terdeteksi";
    document.getElementById('txt-summary-subtitle').textContent = `${petLabel} · ${data.total_gejala} gejala terpilih`;
    cardsContainer.innerHTML = `
      <div class="healthy-panel">
        <h4>Kondisi Hewan Terdeteksi Sehat</h4>
        <p>Gejala yang dimasukkan tidak memenuhi ambang batas minimum (min: 2 gejala kunci) untuk mendiagnosis Toxoplasmosis maupun Rabies.</p>
      </div>`;
  } else {
    document.getElementById('txt-summary-title').textContent = `${data.hasil.length} Penyakit Terindikasi`;
    document.getElementById('txt-summary-subtitle').textContent = `${petLabel} · ${data.total_gejala} gejala terpilih`;
    cardsContainer.innerHTML = data.hasil.map(report => buildDiseaseCard(report, data.hewan)).join('');
  }
}

function buildDiseaseCard(report, pet) {
  const matchedPills = report.gejala_cocok.map(gid =>
    `<span class="symptom-pill matched" title="${GEJALA[gid]}">${gid}: ${GEJALA[gid]}</span>`
  ).join('');
  const unmatchedPills = report.gejala_tidak.slice(0, 5).map(gid =>
    `<span class="symptom-pill unmatched" title="${GEJALA[gid]}">${gid}: ${GEJALA[gid]}</span>`
  ).join('');
  const treatmentItems = report.penanganan.map(step => {
    const isEmergency = step.startsWith('DARURAT') || step.startsWith('JANGAN');
    return `<div class="treatment-item ${isEmergency ? 'emergency' : ''}">
      <span class="treatment-item-bullet">${isEmergency ? '⚠️' : '→'}</span>
      <span>${step}</span>
    </div>`;
  }).join('');
  return `
    <div class="disease-report-card" style="border-top: 4px solid ${report.warna}">
      <div class="disease-header">
        <div>
          <span class="disease-badge-code">Kode Penyakit: ${report.id}</span>
          <h4 class="disease-info-title">${report.nama}</h4>
        </div>
        <div style="text-align: right;">
          <span class="confidence-level-text" style="color: ${report.warna}">${report.tingkat}</span>
        </div>
      </div>
      <div class="disease-body">
        <div class="confidence-meter-container" style="margin-bottom: 1.25rem;">
          <div class="confidence-meta">
            <span style="font-size: 0.72rem; color: var(--text-muted); font-weight:600;">Persentase Keyakinan (Skor)</span>
            <span class="confidence-badge-value" style="color: ${report.warna}">${report.keyakinan}%</span>
          </div>
          <div class="confidence-meter-bar">
            <div class="confidence-meter-fill" style="width: ${report.keyakinan}%; background-color: ${report.warna};"></div>
          </div>
        </div>
        <div class="disease-body-section">
          <span class="section-headline">Deskripsi Penyakit</span>
          <p class="disease-desc-text">${report.deskripsi}</p>
        </div>
        <div class="disease-body-section">
          <span class="section-headline">Gejala Terindikasi (${report.jumlah_cocok} Gejala)</span>
          <div class="symptom-tag-cloud">${matchedPills}</div>
        </div>
        ${unmatchedPills ? `<div class="disease-body-section">
          <span class="section-headline">Gejala Tidak Terdeteksi</span>
          <div class="symptom-tag-cloud">${unmatchedPills}</div>
        </div>` : ''}
        <div class="disease-body-section">
          <span class="section-headline">Saran &amp; Penanganan Medis</span>
          <div class="treatment-steps">${treatmentItems}</div>
        </div>
      </div>
    </div>`;
}

function showLoading(visible) {
  document.getElementById('block-loading').style.display = visible ? 'block' : 'none';
  if (visible) { document.getElementById('panel-empty-state').style.display = 'none'; }
}

function hideDiagnosis() {
  document.getElementById('panel-empty-state').style.display = 'flex';
  document.getElementById('panel-results-output').style.display = 'none';
  document.getElementById('container-disease-cards').innerHTML = '';
}
