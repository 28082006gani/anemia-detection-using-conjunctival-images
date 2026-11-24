/**
 * validate.js - Client-side form hints and interactive checks
 */
document.addEventListener('DOMContentLoaded', function () {
  const nameInput = document.getElementById('patient_name');
  const ageInput = document.getElementById('patient_age');
  const placeInput = document.getElementById('patient_place');

  const nameHint = document.getElementById('name-hint');
  const ageHint = document.getElementById('age-hint');
  const placeHint = document.getElementById('place-hint');

  if (nameInput && nameHint) {
    nameInput.addEventListener('input', function () {
      const val = this.value.trim();
      if (val.length === 0) {
        nameHint.textContent = '2–80 letters and characters';
        nameHint.style.color = 'var(--muted)';
      } else if (val.length < 2 || val.length > 80) {
        nameHint.textContent = 'Name must be between 2 and 80 characters';
        nameHint.style.color = 'var(--alert)';
      } else if (!/^[A-Za-z\s.'-]+$/.test(val)) {
        nameHint.textContent = 'Name contains invalid characters (letters, spaces, hyphens only)';
        nameHint.style.color = 'var(--alert)';
      } else {
        nameHint.textContent = 'Valid name';
        nameHint.style.color = 'var(--ok)';
      }
    });
  }

  if (ageInput && ageHint) {
    ageInput.addEventListener('input', function () {
      const val = parseInt(this.value, 10);
      if (isNaN(val)) {
        ageHint.textContent = '0–120';
        ageHint.style.color = 'var(--muted)';
      } else if (val < 0 || val > 120) {
        ageHint.textContent = 'Age must be between 0 and 120';
        ageHint.style.color = 'var(--alert)';
      } else {
        ageHint.textContent = 'Valid age';
        ageHint.style.color = 'var(--ok)';
      }
    });
  }

  // Place/Location validation and live feedback is handled by location_autocomplete.js
});
