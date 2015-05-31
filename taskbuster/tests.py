# -*- coding: utf-8 -*-
import os

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import activate


class TestHomePage(TestCase):
    def _activate():
        activate(settings.LANGUAGES[0][0])
        
    def test_uses_index_template(self):
        for l in settings.LANGUAGES: 
            activate(l[0])
            response = self.client.get(reverse("home"))
            self.assertTemplateUsed(response, "taskbuster/index.html")
        
    def test_uses_base_template(self):
        for l in settings.LANGUAGES: 
            activate(l[0])        
            response = self.client.get(reverse("home"))
            self.assertTemplateUsed(response, "base.html")
            
  
            
class TestSettingsForTranslations(TestCase):
    
    def test_settings_has_required_setings_for_translations(self):
        self.assertEqual(settings.USE_I18N,True)
        self.assertIn('django.middleware.locale.LocaleMiddleware',settings.MIDDLEWARE_CLASSES)
        self.assertGreaterEqual(len(settings.LANGUAGES),1)
        self.assertEqual(len(settings.LANGUAGES[0]),2)
        self.assertRegex(settings.LANGUAGE_CODE,'[a-z]+.*')
        for path in settings.LOCALE_PATHS:
            self.assertTrue(os.path.exists(path))
            
    def  test_LANGUAGE_CODE_in_LANGUAGES(self):
        language_codes=[x[0] for x in settings.LANGUAGES]
        self.assertIn(settings.LANGUAGE_CODE,language_codes)
            
        
   