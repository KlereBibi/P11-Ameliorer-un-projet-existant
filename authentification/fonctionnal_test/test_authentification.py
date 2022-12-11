from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By


class TestAuthentificationSendResetPassword(StaticLiveServerTestCase):
    def test_reset(self):
        # Ouvrir le navigateur avec le webdriver
        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("authentification:reset_password"))

        password1 = self.browser.find_element(By.ID, "id_email")
        password1.send_keys("test@gmail.com")

        signup = self.browser.find_element(By.ID, "Envoyer")
        signup.click()

        self.assertEqual(self.browser.find_element(By.TAG_NAME, 'h2').text,
                         "La réinitialisation du mot de passe a été envoyé")
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse("authentification:password_reset_done"))


class TestAuthentificationRegister(StaticLiveServerTestCase):
    def test_signup(self):
        # Ouvrir le navigateur avec le webdriver
        self.browser = webdriver.Chrome("authentification/functional_tests/chromedriver")
        self.browser.get(self.live_server_url + reverse("authentification:register"))

        fname = self.browser.find_element(By.ID, "id_first_name")
        fname.send_keys("Claire")
        lname = self.browser.find_element(By.ID, "id_last_name")
        lname.send_keys("Etudiante")
        username = self.browser.find_element(By.ID, "id_username")
        username.send_keys("cEtudiante")
        email = self.browser.find_element(By.ID, "id_email")
        email.send_keys(By.ID, "test@test.com")
        password1 = self.browser.find_element(By.ID, "id_password1")
        password1.send_keys("password@10")
        password2 = self.browser.find_element(By.ID, "id_password2")
        password2.send_keys("password@10")
        signup = self.browser.find_element(By.ID, "submit")
        signup.click()

        self.assertEqual(self.browser.find_element(By.ID, 'confirmation_text').text,
                         "Un courriel vous a été envoyé. Merci de confirmer votre adresse mail pour compléter votre enregistrement.")
        self.assertEqual(self.browser.current_url,
                         self.live_server_url + reverse("authentification:register"))
        # Fermer le navigateur
        self.browser.close()
