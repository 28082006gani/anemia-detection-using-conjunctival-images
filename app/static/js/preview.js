/**
 * preview.js - Client-side image handling, input mode tab switching,
 * and high-fidelity specimen preview.
 */
document.addEventListener('DOMContentLoaded', function () {
  const uploadZone = document.getElementById('panel-file-uploader');
  const scannerLauncher = document.getElementById('panel-scanner-launcher');
  const tabModeCamera = document.getElementById('tab-mode-camera');
  const tabModeUpload = document.getElementById('tab-mode-upload');

  const fileInput = document.getElementById('image-input');
  const previewBox = document.getElementById('preview-box');
  const previewImg = document.getElementById('preview-img');
  const previewFilename = document.getElementById('preview-filename');
  const previewFilesize = document.getElementById('preview-filesize');
  const btnClear = document.getElementById('btn-clear-image');
  const scanForm = document.getElementById('scan-form');
  const btnSubmit = document.getElementById('btn-submit-scan');
  const btnText = document.getElementById('btn-text');

  let activeMode = 'camera'; // 'camera' or 'upload'

  function updateModeUI() {
    if (activeMode === 'camera') {
      if (tabModeCamera) {
        tabModeCamera.classList.add('active');
        tabModeCamera.setAttribute('aria-selected', 'true');
      }
      if (tabModeUpload) {
        tabModeUpload.classList.remove('active');
        tabModeUpload.setAttribute('aria-selected', 'false');
      }
      if (scannerLauncher) scannerLauncher.style.display = 'flex';
      if (uploadZone) uploadZone.style.display = 'none';
    } else {
      if (tabModeUpload) {
        tabModeUpload.classList.add('active');
        tabModeUpload.setAttribute('aria-selected', 'true');
      }
      if (tabModeCamera) {
        tabModeCamera.classList.remove('active');
        tabModeCamera.setAttribute('aria-selected', 'false');
      }
      if (uploadZone) uploadZone.style.display = 'block';
      if (scannerLauncher) scannerLauncher.style.display = 'none';
    }
  }

  if (tabModeCamera) {
    tabModeCamera.addEventListener('click', function () {
      activeMode = 'camera';
      updateModeUI();
    });
  }

  if (tabModeUpload) {
    tabModeUpload.addEventListener('click', function () {
      activeMode = 'upload';
      updateModeUI();
    });
  }

  function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  function handleFile(file) {
    if (!file) return;

    // Check extension
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
      alert('Please select a valid PNG or JPG/JPEG image.');
      fileInput.value = '';
      return;
    }

    // Check size limit: 5MB
    if (file.size > 5 * 1024 * 1024) {
      alert('The selected image exceeds the 5 MB size limit.');
      fileInput.value = '';
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      if (previewImg) previewImg.src = e.target.result;
      if (previewFilename) previewFilename.textContent = file.name;
      if (previewFilesize) previewFilesize.textContent = `${formatBytes(file.size)} · Ready for Deep Learning Analysis`;
      if (previewBox) previewBox.style.display = 'flex';
    };
    reader.readAsDataURL(file);
  }

  if (fileInput) {
    fileInput.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        handleFile(this.files[0]);
      }
    });
  }

  // Drag and drop events on upload zone
  if (uploadZone) {
    uploadZone.addEventListener('click', function () {
      if (fileInput) fileInput.click();
    });

    ['dragenter', 'dragover'].forEach(eventName => {
      uploadZone.addEventListener(eventName, function (e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      uploadZone.addEventListener(eventName, function (e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.classList.remove('dragover');
      }, false);
    });

    uploadZone.addEventListener('drop', function (e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files[0]) {
        fileInput.files = files;
        handleFile(files[0]);
      }
    });
  }

  if (btnClear) {
    btnClear.addEventListener('click', function () {
      if (fileInput) fileInput.value = '';
      if (previewImg) previewImg.src = '';
      if (previewFilename) previewFilename.textContent = '';
      if (previewFilesize) previewFilesize.textContent = '';
      if (previewBox) previewBox.style.display = 'none';
      updateModeUI();
    });
  }

  // Loading state on form submission
  if (scanForm && btnSubmit) {
    scanForm.addEventListener('submit', function (e) {
      if (!fileInput || fileInput.files.length === 0) {
        alert('Please scan an image or upload a conjunctival photo before running screening.');
        e.preventDefault();
        return;
      }

      btnSubmit.disabled = true;
      if (btnText) {
        btnText.textContent = 'Processing Biometric Analysis…';
      }
    });
  }
});
