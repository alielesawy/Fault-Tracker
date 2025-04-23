from flask import session, request, g
from functools import wraps
from translations import ar, en
from config import Config

# Dictionary of available translations
translations = {
    'ar': ar,
    'en': en
}

def get_locale():
    """Get the current locale from session or default to config setting."""
    if 'language' in session:
        return session['language']
    return Config.DEFAULT_LANGUAGE

def set_locale(locale):
    """Set the locale in session."""
    if locale in Config.LANGUAGES:
        session['language'] = locale

def get_text(key, **kwargs):
    """Get text from the current language dictionary."""
    locale = get_locale()
    if locale not in translations or key not in translations[locale]:
        # Fallback to English or return the key as is
        locale = 'en'
        if key not in translations[locale]:
            return key
    
    text = translations[locale][key]
    
    # Format with any provided kwargs
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text

def with_language(f):
    """Decorator to set language context for each request."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for language parameter in URL
        lang = request.args.get('lang')
        if lang and lang in Config.LANGUAGES:
            set_locale(lang)
        
        # Store translation function in g for easy access in templates
        g._ = get_text
        
        # Set RTL/LTR direction based on language
        g.is_rtl = get_locale() == 'ar'
        
        return f(*args, **kwargs)
    return decorated_function

# Add shorthand names for convenience
_ = get_text