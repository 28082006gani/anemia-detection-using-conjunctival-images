/**
 * camera.js - Scan Image Using Camera with live viewfinder,
 * permission handling, device switching, capture, retake & confirmation.
 */
document.addEventListener('DOMContentLoaded', function () {
  const btnOpenCamera = document.getElementById('btn-open-camera');
  const modalOverlay = document.getElementById('camera-modal');
  const btnCloseModal = document.getElementById('btn-close-camera');
  const videoEl = document.getElementById('camera-video');
  const canvasEl = document.getElementById('camera-canvas');
  const capturedImgEl = document.getElementById('camera-captured-img');
  const guideOverlay = document.getElementById('camera-guide-overlay');

  const btnCapture = document.getElementById('btn-capture-photo');
  const btnSwitchCam = document.getElementById('btn-switch-cam');
  const btnCancelScan = document.getElementById('btn-cancel-scan');

  const reviewActions = document.getElementById('camera-review-actions');
  const liveControls = document.getElementById('camera-live-controls');
  const btnRetake = document.getElementById('btn-retake-photo');
  const btnConfirm = document.getElementById('btn-confirm-photo');

  const errorContainer = document.getElementById('camera-error-container');
  const errorTitle = document.getElementById('camera-error-title');
  const errorDesc = document.getElementById('camera-error-desc');
  const btnRetry = document.getElementById('btn-retry-camera');
  const nativeCameraInput = document.getElementById('camera-native-input');

  const fileInput = document.getElementById('image-input');

  if (!btnOpenCamera || !modalOverlay) return;

  let activeStream = null;
  let currentFacingMode = 'environment'; // prefer rear/environment camera for eye photos
  let capturedBlob = null;

  function stopStream() {
    if (activeStream) {
      activeStream.getTracks().forEach(track => {
        try {
          track.stop();
        } catch (e) {}
      });
      activeStream = null;
    }
    if (videoEl) {
      videoEl.srcObject = null;
    }
  }

  function closeModal() {
    stopStream();
    modalOverlay.classList.remove('active');
    capturedBlob = null;
    if (capturedImgEl) {
      capturedImgEl.style.display = 'none';
      capturedImgEl.src = '';
    }
    if (videoEl) {
      videoEl.style.display = 'block';
    }
    if (guideOverlay) {
      guideOverlay.style.display = 'flex';
    }
    if (liveControls) liveControls.style.display = 'flex';
    if (reviewActions) reviewActions.style.display = 'none';
    if (errorContainer) errorContainer.style.display = 'none';
  }

  async function startCamera() {
    stopStream();
    if (errorContainer) errorContainer.style.display = 'none';
    if (videoEl) videoEl.style.display = 'block';
    if (guideOverlay) guideOverlay.style.display = 'flex';
    if (capturedImgEl) capturedImgEl.style.display = 'none';
    if (liveControls) liveControls.style.display = 'flex';
    if (reviewActions) reviewActions.style.display = 'none';

    // Verify browser support for getUserMedia
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      // Fallback: trigger native file camera capture directly on mobile
      if (nativeCameraInput) {
        closeModal();
        nativeCameraInput.click();
        return;
      }
      showCameraError(
        'Camera API Not Supported',
        'Your browser does not support in-browser camera streaming. Please upload an image directly.'
      );
      return;
    }

    try {
      const constraints = {
        video: {
          facingMode: { ideal: currentFacingMode },
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      activeStream = stream;
      videoEl.srcObject = stream;
      await videoEl.play();

      // Check if multiple camera devices exist for the switch camera button
      try {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter(d => d.kind === 'videoinput');
        if (btnSwitchCam) {
          btnSwitchCam.style.display = videoDevices.length > 1 ? 'inline-flex' : 'none';
        }
      } catch (devErr) {
        if (btnSwitchCam) btnSwitchCam.style.display = 'none';
      }
    } catch (err) {
      console.warn('Camera access error:', err);
      let title = 'Camera Access Required';
      let message = 'Please grant camera permissions in your browser to scan the conjunctival image.';

      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        title = 'Camera Permission Denied';
        message = 'Camera access was blocked. To scan an image, please allow camera permission in your browser URL bar or settings, then click "Try Again".';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        title = 'No Camera Detected';
        message = 'No camera device was found on this system. You can choose a photo from your gallery instead.';
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        title = 'Camera Already In Use';
        message = 'The camera is currently being used by another application or tab. Please close other camera apps and retry.';
      }

      showCameraError(title, message);
    }
  }

  function showCameraError(title, desc) {
    if (videoEl) videoEl.style.display = 'none';
    if (guideOverlay) guideOverlay.style.display = 'none';
    if (liveControls) liveControls.style.display = 'none';
    if (reviewActions) reviewActions.style.display = 'none';

    if (errorContainer) {
      errorTitle.textContent = title;
      errorDesc.textContent = desc;
      errorContainer.style.display = 'flex';
    }
  }

  function capturePhoto() {
    if (!videoEl || !canvasEl) return;

    const width = videoEl.videoWidth || 1280;
    const height = videoEl.videoHeight || 720;

    canvasEl.width = width;
    canvasEl.height = height;
    const ctx = canvasEl.getContext('2d');
    ctx.drawImage(videoEl, 0, 0, width, height);

    canvasEl.toBlob(function (blob) {
      if (!blob) {
        alert('Could not capture frame. Please try again.');
        return;
      }
      capturedBlob = blob;

      // Display preview of captured image
      const previewUrl = URL.createObjectURL(blob);
      capturedImgEl.src = previewUrl;
      capturedImgEl.style.display = 'block';
      videoEl.style.display = 'none';
      guideOverlay.style.display = 'none';

      // Switch control buttons to Confirm / Retake
      liveControls.style.display = 'none';
      reviewActions.style.display = 'flex';
    }, 'image/jpeg', 0.95);
  }

  function confirmCapturedPhoto() {
    if (!capturedBlob || !fileInput) return;

    // Create a real File instance
    const timestamp = new Date().toISOString().replace(/[-:.]/g, '').slice(0, 15);
    const fileName = `conjunctiva_scan_${timestamp}.jpg`;
    const file = new File([capturedBlob], fileName, { type: 'image/jpeg' });

    // Assign to file input using DataTransfer
    try {
      const dt = new DataTransfer();
      dt.items.add(file);
      fileInput.files = dt.files;
      // Trigger change event so preview.js updates the thumbnail immediately
      fileInput.dispatchEvent(new Event('change', { bubbles: true }));
    } catch (e) {
      console.error('DataTransfer assignment failed:', e);
    }

    closeModal();
  }

  // Open modal & start camera
  btnOpenCamera.addEventListener('click', function () {
    modalOverlay.classList.add('active');
    startCamera();
  });

  if (btnCloseModal) btnCloseModal.addEventListener('click', closeModal);
  if (btnCancelScan) btnCancelScan.addEventListener('click', closeModal);

  if (btnRetry) {
    btnRetry.addEventListener('click', function () {
      startCamera();
    });
  }

  if (btnCapture) {
    btnCapture.addEventListener('click', capturePhoto);
  }

  if (btnRetake) {
    btnRetake.addEventListener('click', function () {
      capturedBlob = null;
      startCamera();
    });
  }

  if (btnConfirm) {
    btnConfirm.addEventListener('click', confirmCapturedPhoto);
  }

  if (btnSwitchCam) {
    btnSwitchCam.addEventListener('click', function () {
      currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
      startCamera();
    });
  }

  // Handle native fallback input change (e.g. mobile native camera capture)
  if (nativeCameraInput) {
    nativeCameraInput.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        try {
          const dt = new DataTransfer();
          dt.items.add(this.files[0]);
          fileInput.files = dt.files;
          fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        } catch (e) {}
      }
    });
  }

  // Close modal when pressing Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
      closeModal();
    }
  });
});
