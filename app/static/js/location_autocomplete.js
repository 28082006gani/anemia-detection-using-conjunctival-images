/**
 * location_autocomplete.js
 * Smart City/Village Autocomplete with debounced live search,
 * keyboard navigation, highlight matching, and location verification.
 */
document.addEventListener('DOMContentLoaded', function () {
  const placeInput = document.getElementById('patient_place');
  const dropdown = document.getElementById('location-dropdown');
  const spinner = document.getElementById('location-spinner');
  const placeHint = document.getElementById('place-hint');
  const cityInput = document.getElementById('patient_city');
  const stateInput = document.getElementById('patient_state');
  const countryInput = document.getElementById('patient_country');
  const scanForm = document.getElementById('scan-form');
  const btnSubmit = document.getElementById('btn-submit-scan');
  const btnText = document.getElementById('btn-text');

  if (!placeInput || !dropdown) return;

  let debounceTimer = null;
  let currentController = null;
  let activeIndex = -1;
  let currentResults = [];
  let isVerified = Boolean(cityInput && cityInput.value && placeInput.value);

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function highlightText(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    return text.replace(regex, '<span class="highlight">$1</span>');
  }

  function closeDropdown() {
    dropdown.style.display = 'none';
    dropdown.innerHTML = '';
    activeIndex = -1;
    currentResults = [];
  }

  function selectLocation(loc) {
    placeInput.value = loc.display;
    if (cityInput) cityInput.value = loc.city;
    if (stateInput) stateInput.value = loc.state;
    if (countryInput) countryInput.value = loc.country;
    isVerified = true;

    if (placeHint) {
      placeHint.innerHTML = `<span class="location-verified">✓ Verified location: ${loc.city}, ${loc.state}, ${loc.country}</span>`;
    }
    closeDropdown();
  }

  function renderResults(results, query) {
    dropdown.innerHTML = '';
    currentResults = results;
    activeIndex = -1;

    if (!results || results.length === 0) {
      const emptyLi = document.createElement('li');
      emptyLi.className = 'autocomplete-empty';
      emptyLi.textContent = 'No matching locations found';
      dropdown.appendChild(emptyLi);
      dropdown.style.display = 'block';
      return;
    }

    results.forEach((loc, index) => {
      const li = document.createElement('li');
      li.className = 'autocomplete-item';
      li.setAttribute('role', 'option');
      li.setAttribute('id', `loc-opt-${index}`);

      const nameDiv = document.createElement('div');
      nameDiv.className = 'autocomplete-item-name';
      nameDiv.innerHTML = highlightText(loc.city, query);

      const subDiv = document.createElement('div');
      subDiv.className = 'autocomplete-item-sub';
      subDiv.innerHTML = highlightText(`${loc.state}, ${loc.country}`, query);

      li.appendChild(nameDiv);
      li.appendChild(subDiv);

      li.addEventListener('mouseenter', () => {
        setActiveIndex(index);
      });

      li.addEventListener('click', (e) => {
        e.preventDefault();
        selectLocation(loc);
      });

      dropdown.appendChild(li);
    });

    dropdown.style.display = 'block';
  }

  function setActiveIndex(index) {
    const items = dropdown.querySelectorAll('.autocomplete-item');
    items.forEach(el => el.classList.remove('active'));
    activeIndex = index;

    if (activeIndex >= 0 && activeIndex < items.length) {
      items[activeIndex].classList.add('active');
      items[activeIndex].scrollIntoView({ block: 'nearest' });
    }
  }

  async function fetchLocations(query) {
    if (spinner) spinner.style.display = 'block';

    if (currentController) {
      currentController.abort();
    }
    currentController = new AbortController();

    try {
      const res = await fetch(`/api/locations/search?q=${encodeURIComponent(query)}`, {
        signal: currentController.signal
      });
      if (!res.ok) throw new Error('Network error');
      const data = await res.json();
      renderResults(data, query);
    } catch (err) {
      if (err.name !== 'AbortError') {
        dropdown.innerHTML = '<li class="autocomplete-empty">Unable to fetch locations. Please retry.</li>';
        dropdown.style.display = 'block';
      }
    } finally {
      if (spinner) spinner.style.display = 'none';
    }
  }

  placeInput.addEventListener('input', function () {
    const val = this.value.trim();
    isVerified = false;

    if (cityInput) cityInput.value = '';
    if (stateInput) stateInput.value = '';

    if (val.length < 2) {
      closeDropdown();
      if (spinner) spinner.style.display = 'none';
      if (placeHint) {
        placeHint.innerHTML = 'Type at least 2 letters (e.g. Dav, Ban, Mum)';
        placeHint.className = 'form-hint';
      }
      return;
    }

    if (placeHint) {
      placeHint.innerHTML = 'Searching cities and villages…';
      placeHint.className = 'form-hint';
    }

    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      fetchLocations(val);
    }, 250);
  });

  // Keyboard navigation
  placeInput.addEventListener('keydown', function (e) {
    const items = dropdown.querySelectorAll('.autocomplete-item');
    if (dropdown.style.display === 'none' || items.length === 0) {
      return;
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      const next = activeIndex + 1 >= items.length ? 0 : activeIndex + 1;
      setActiveIndex(next);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      const prev = activeIndex - 1 < 0 ? items.length - 1 : activeIndex - 1;
      setActiveIndex(prev);
    } else if (e.key === 'Enter') {
      if (activeIndex >= 0 && activeIndex < currentResults.length) {
        e.preventDefault();
        selectLocation(currentResults[activeIndex]);
      }
    } else if (e.key === 'Escape') {
      closeDropdown();
    }
  });

  // Close dropdown on click outside
  document.addEventListener('click', function (e) {
    if (!placeInput.contains(e.target) && !dropdown.contains(e.target)) {
      closeDropdown();
    }
  });

  // Require selection from dropdown upon form submit
  if (scanForm) {
    scanForm.addEventListener('submit', function (e) {
      const val = placeInput.value.trim();
      if (!val) return; // handled by required attribute

      // If user typed something but did not click/select from suggestions
      if (!isVerified || !cityInput.value) {
        // Check if exact match exists in current results
        const exactMatch = currentResults.find(
          r => r.display.toLowerCase() === val.toLowerCase() ||
               r.city.toLowerCase() === val.toLowerCase()
        );

        if (exactMatch) {
          selectLocation(exactMatch);
        } else {
          e.preventDefault();
          alert('Please select a valid city or village from the search suggestions dropdown.');
          placeInput.focus();

          if (placeHint) {
            placeHint.innerHTML = '<span class="location-unverified">Please select a location from the dropdown suggestions.</span>';
          }

          if (btnSubmit) {
            btnSubmit.disabled = false;
            if (btnText) btnText.textContent = 'Analyse image';
          }
          return false;
        }
      }
    });
  }
});
