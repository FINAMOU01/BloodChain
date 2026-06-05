(function () {
    function getStoredUser() {
        try {
            return JSON.parse(localStorage.getItem('user') || 'null');
        } catch (error) {
            return null;
        }
    }

    function getDonorEmail() {
        const user = getStoredUser();
        return localStorage.getItem('donor_email') || (user && user.email) || '';
    }

    function logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('donor_email');
        localStorage.removeItem('hospital_email');
        window.location.replace('/login/');
    }

    function requireAuth() {
        const donorEmail = getDonorEmail();
        if (!localStorage.getItem('token') || !donorEmail) {
            window.location.replace('/login/');
            return '';
        }
        return donorEmail;
    }

    function setupShell() {
        const donorEmail = getDonorEmail();
        document.querySelectorAll('.logout-link').forEach(link => {
            link.setAttribute('href', '/login/');
            link.addEventListener('click', event => {
                event.preventDefault();
                logout();
            });
        });

        document.querySelectorAll('.sidebar-footer p').forEach(name => {
            name.textContent = donorEmail || 'Donor';
        });

        document.querySelectorAll('.topbar-avatar').forEach(avatar => {
            avatar.textContent = donorEmail ? donorEmail.charAt(0).toUpperCase() : 'D';
        });

        document.querySelectorAll('.topbar-date').forEach(dateElement => {
            dateElement.textContent = new Date().toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
                year: 'numeric'
            });
        });
    }

    function updateNotificationBadges(donorEmail) {
        return fetch('/api/notifications/list/')
            .then(response => response.json())
            .then(notifications => {
                const visible = notifications.filter(item => item.recipient_email === donorEmail || !item.recipient_email);
                const count = visible.filter(item => !item.is_sent).length;
                document.querySelectorAll('.nav-badge, .notification-badge').forEach(badge => {
                    badge.textContent = count || '';
                });
                return visible;
            })
            .catch(() => []);
    }

    window.BloodChainDonor = {
        getDonorEmail,
        logout,
        requireAuth,
        setupShell,
        updateNotificationBadges
    };
})();
