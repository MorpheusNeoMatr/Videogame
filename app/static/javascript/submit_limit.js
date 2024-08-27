document.addEventListener('DOMContentLoaded', () => {
    const forms = [
        {formId: 'submit_series_form', buttonId: 'submit-series-Button'},
        {formId: 'submit_genre_form', buttonId: 'submit-genre-Button'},
        {formId: 'submit_game_form', buttonId: 'submit-game-Button'},
        {formId: 'submit_register_form', buttonId: 'submit-register-Button'},
        {formId: 'submit_company_form', buttonId: 'submit-company-Button'},
        {formId: 'submit_games_series_form', buttonId: 'submit-games-series-Button'},
        {formId: 'submit_games_genre_form', buttonId: 'submit-games-genre-Button'},
        {formId: 'submit_company_series_form', buttonId: 'submit-company-series-Button'},
        {formId: 'submit_director_form', buttonId: 'submit-director-Button'},
        {formId: 'submit_founder_form', buttonId: 'submit-founder-Button'},
        {formId: 'submit_login_form', buttonId: 'submit-login-Button'}
    ];

    forms.forEach(({formId, buttonId}) => {
        const form = document.getElementById(formId);
        const submitButton = document.getElementById(buttonId);

        if (form && submitButton) { // Check if elements are found
            form.addEventListener('submit', (event) => {
                submitButton.disabled = true;
                submitButton.textContent = 'Submitting...'; // Optional: Change button text
            });
        } else {
            console.log(`Form or button not found: ${formId} - ${buttonId}`);
        }
    });
});
