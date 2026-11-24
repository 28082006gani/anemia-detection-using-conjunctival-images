/**
 * ANEMIASCAN - AUTHENTICATION & LOGIN UI INTERACTIONS
 * Handles 3D tilt perspective, traveling beam reactivity, password visibility toggle,
 * and seamless tab transitions between Sign In and Create Account.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Enable white-and-blue gradient theme on auth page
  document.body.classList.add('auth-dark-mode');
  document.body.classList.add('auth-gradient-theme');

  // 2. 3D Card Tilt based on mouse movement
  const scene = document.getElementById('card3dScene');
  const tilt = document.getElementById('card3dTilt');

  if (scene && tilt) {
    scene.addEventListener('mousemove', function (e) {
      const rect = tilt.getBoundingClientRect();
      const mouseX = e.clientX - rect.left - rect.width / 2;
      const mouseY = e.clientY - rect.top - rect.height / 2;

      // Calculate 3D rotation angles (-8deg to 8deg)
      const rotateX = -(mouseY / (rect.height / 2)) * 8;
      const rotateY = (mouseX / (rect.width / 2)) * 8;

      tilt.style.transform = `perspective(1500px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(8px)`;
    });

    scene.addEventListener('mouseleave', function () {
      tilt.style.transform = 'perspective(1500px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
    });
  }

  // 3. Password visibility toggles
  const eyeButtons = document.querySelectorAll('.btn-pwd-eye');
  eyeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const targetId = btn.getAttribute('data-target');
      if (!targetId) return;
      const input = document.getElementById(targetId);
      if (!input) return;

      const eyeOpen = btn.querySelector('.eye-open-icon');
      const eyeClosed = btn.querySelector('.eye-closed-icon');

      if (input.type === 'password') {
        input.type = 'text';
        if (eyeOpen) eyeOpen.style.display = 'none';
        if (eyeClosed) eyeClosed.style.display = 'block';
      } else {
        input.type = 'password';
        if (eyeOpen) eyeOpen.style.display = 'block';
        if (eyeClosed) eyeClosed.style.display = 'none';
      }
    });
  });

  // 4. Input field focus highlights
  const textInputs = document.querySelectorAll('.card-text-input');
  textInputs.forEach(function (input) {
    input.addEventListener('focus', function () {
      const group = input.closest('.input-field-group');
      if (group) group.classList.add('focused');
    });
    input.addEventListener('blur', function () {
      const group = input.closest('.input-field-group');
      if (group) group.classList.remove('focused');
    });
  });

  // 5. Tab switching between Sign in and Create Account
  const pillLogin = document.getElementById('pillLogin');
  const pillRegister = document.getElementById('pillRegister');
  const paneLogin = document.getElementById('paneLogin');
  const paneRegister = document.getElementById('paneRegister');
  const title = document.getElementById('authCardTitle');
  const subtitle = document.getElementById('authCardSubtitle');
  const linkToRegister = document.getElementById('linkToRegister');
  const linkToLogin = document.getElementById('linkToLogin');

  function switchTab(tab, updateHistory = true) {
    if (tab === 'register') {
      if (pillLogin) {
        pillLogin.classList.remove('active');
        pillLogin.setAttribute('aria-selected', 'false');
      }
      if (paneLogin) paneLogin.classList.remove('active');

      if (pillRegister) {
        pillRegister.classList.add('active');
        pillRegister.setAttribute('aria-selected', 'true');
      }
      if (paneRegister) paneRegister.classList.add('active');
      if (title) title.textContent = 'Create Account';
      if (subtitle) subtitle.textContent = 'Register for non-invasive conjunctival screening';

      const regEmail = document.getElementById('register-email');
      if (regEmail) regEmail.focus();

      if (updateHistory) {
        window.history.replaceState(null, '', '/register');
      }
    } else {
      if (pillRegister) {
        pillRegister.classList.remove('active');
        pillRegister.setAttribute('aria-selected', 'false');
      }
      if (paneRegister) paneRegister.classList.remove('active');

      if (pillLogin) {
        pillLogin.classList.add('active');
        pillLogin.setAttribute('aria-selected', 'true');
      }
      if (paneLogin) paneLogin.classList.add('active');
      if (title) title.textContent = 'Welcome to AnemiaScan';
      if (subtitle) subtitle.textContent = 'Sign in to continue to AnemiaScan';

      const logEmail = document.getElementById('login-email');
      if (logEmail) logEmail.focus();

      if (updateHistory) {
        window.history.replaceState(null, '', '/login');
      }
    }
  }

  if (pillLogin) {
    pillLogin.addEventListener('click', function () { switchTab('login'); });
  }
  if (pillRegister) {
    pillRegister.addEventListener('click', function () { switchTab('register'); });
  }
  if (linkToRegister) {
    linkToRegister.addEventListener('click', function (e) {
      e.preventDefault();
      switchTab('register');
    });
  }
  if (linkToLogin) {
    linkToLogin.addEventListener('click', function (e) {
      e.preventDefault();
      switchTab('login');
    });
  }

  // 6. Secondary buttons (Forgot Password & Google SSO)
  const forgotBtn = document.getElementById('forgotPwdLink');
  if (forgotBtn) {
    forgotBtn.addEventListener('click', function (e) {
      e.preventDefault();
      alert('Password reset instructions: Please contact your clinic administrator or screening system supervisor.');
    });
  }

  const googleBtn = document.getElementById('googleSignInBtn');
  if (googleBtn) {
    googleBtn.addEventListener('click', function () {
      alert('Google Workspace single sign-on is enabled for institutional hospital deployments.');
    });
  }
});
