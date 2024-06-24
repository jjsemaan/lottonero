from django.test import TestCase
import pytest
from .forms import UnauthenticatedContactMessageForm
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_unauthenticated_contact_message_form():
    """
    Test the behavior of the UnauthenticatedContactMessageForm with various input scenarios.

    This test ensures that:
    - The form is properly initialized with the expected fields ('full_name', 'email', 'message').
    - It validates correctly when provided with valid data.
    - All fields are correctly included in the form when instantiated.
    - The 'email' field remains visible and part of the form even when simulating an unauthenticated user.

    Steps:
    1. Create a form instance with predefined valid data and verify its validity.
    2. Assert that all expected fields are present in the form.
    3. Simulate an unauthenticated user by creating a form instance with an AnonymousUser and check form validity and fields.
    """
    form_data = {'full_name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello there'}
    form = UnauthenticatedContactMessageForm(data=form_data)
    assert form.is_valid(), form.errors

    assert 'full_name' in form.fields
    assert 'email' in form.fields
    assert 'message' in form.fields

    user = AnonymousUser()
    form = UnauthenticatedContactMessageForm(data=form_data, user=user)
    assert form.is_valid(), form.errors
    assert 'email' in form.fields


@pytest.mark.django_db
def test_authenticated_contact_message_form():
    """
    Test the behavior of the AuthenticatedContactMessageForm when used by an authenticated user.

    This test ensures that:
    - The form is correctly initialized with an authenticated user and can validate provided data.
    - Only the appropriate fields ('message') are included in the form for authenticated users, 
      confirming that fields irrelevant for authenticated contexts ('full_name', 'email') are absent.

    Steps:
    1. Create a user and authenticate them.
    2. Initialize the form with valid data and a reference to the authenticated user.
    3. Validate the form to ensure it processes the input correctly and adheres to expected validation rules.
    4. Check the presence of the 'message' field and the absence of 'full_name' and 'email' fields 
       to verify that the form adapts its fields based on user authentication status.
    """
    user = User.objects.create_user(username='jane', password='secret')
    form_data = {'message': 'Hi there'}
    form = AuthenticatedContactMessageForm(data=form_data, user=user)
    assert form.is_valid(), form.errors

    assert 'message' in form.fields
    assert 'full_name' not in form.fields
    assert 'email' not in form.fields
