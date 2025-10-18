// ---------------- REGISTER ----------------
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      first_name: document.getElementById('first_name').value,
      last_name: document.getElementById('last_name').value,
      email: document.getElementById('email').value,
      password: document.getElementById('password').value,
      education: document.getElementById('education').value,
      cgpa: document.getElementById('cgpa').value
    };

    const res = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const j = await res.json();
    if (res.ok) {
      alert('Registered successfully! Please login.');
      window.location.href = '/login';
    } else {
      alert('Error: ' + (j.error || 'Unable to register.'));
    }
  });
}


// ---------------- LOGIN ----------------
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
      email: document.getElementById('login_email').value,
      password: document.getElementById('login_password').value
    };

    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const j = await res.json();
    if (res.ok) {
      alert('Login successful!');
      window.location.href = '/profile';
    } else {
      alert('Login failed: ' + (j.error || 'Unknown error.'));
    }
  });
}


// ---------------- PROFILE SAVE ----------------
const profileForm = document.getElementById('profileForm');
if (profileForm) {
  profileForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
      skills: document.getElementById('skills').value,
      interests: document.getElementById('interests').value
    };

    const res = await fetch('/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const j = await res.json();
    if (res.ok) {
      alert('Profile updated successfully!');
    } else if (res.status === 401) {
      alert('Please login again.');
      window.location.href = '/login';
    } else {
      alert('Error: ' + (j.error || 'Failed to save profile.'));
    }
  });
}


// ---------------- GO TO RESULTS ----------------
const goRec = document.getElementById('goRecommend');
if (goRec) {
  goRec.addEventListener('click', () => {
    window.location.href = '/results';
  });
}


// ---------------- LOAD RESULTS PAGE ----------------
if (window.location.pathname.endsWith('/results')) {
  fetch('/recommend')
    .then(res => res.json())
    .then(j => {
      if (j.error) {
        alert(j.error);
        window.location.href = '/login';
        return;
      }

      const container = document.getElementById('results');
      if (!j.results || j.results.length === 0) {
        container.innerHTML = '<p>No recommendations yet. Try adding more skills!</p>';
        return;
      }

      j.results.forEach(it => {
        const div = document.createElement('div');
        div.className = 'career-card';
        div.innerHTML = `
          <h3>${it.career.title}</h3>
          <p>${it.career.description}</p>
          <small>Score: ${(it.score * 100).toFixed(1)}%</small>
        `;
        container.appendChild(div);
      });
    })
    .catch(err => {
      console.error(err);
      alert('Failed to load recommendations.');
    });
}
