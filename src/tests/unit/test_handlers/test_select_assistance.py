import json
from unittest.mock import AsyncMock, Mock, patch

import pytest

from bot.constants.messages import SELECT_QUESTION
from bot.constants.states import States
from bot.handlers.assistance import select_assistance

common_settings = {
    "keyboard": Mock(),
    "user_data": {States.GET_USERNAME: "Test_question_type"},
    "context": Mock(),
}


@pytest.mark.asyncio
async def test_select_assistance_response(update, context):
    """Select assistance handler returns correct response unittest."""
    with (
        patch(
            "bot.handlers.assistance.build_question_keyboard",
            new=AsyncMock(return_value=common_settings["keyboard"]),
        ),
        patch(
            "bot.handlers.assistance.parse_callback_data",
            Mock(return_value=("question_type", 1)),
        ),
    ):
        response = await select_assistance(update, context)

    assert response is None, ("Handler select_assistance must return None.",)


@pytest.mark.parametrize(
    "new_question_type, old_question_type, expected_type_saved",
    [
        ("LEGAL_ASSISTANCE", "Test_type", "LEGAL_ASSISTANCE"),
        (None, "LEGAL_ASSISTANCE", "LEGAL_ASSISTANCE"),
    ],
)
@pytest.mark.asyncio
async def test_select_assistance_save_question_type(
    update, new_question_type, old_question_type, expected_type_saved
):
    """Select assistance handler saves question type unittest."""
    update.callback_query.message.reply_markup.to_json = Mock(
        return_value=json.dumps(dict())
    )
    context = common_settings["context"]
    context.user_data = {States.GET_USERNAME: old_question_type}

    with (
        patch(
            "bot.handlers.assistance.build_question_keyboard",
            new=AsyncMock(return_value=common_settings["keyboard"]),
        ),
        patch(
            "bot.handlers.assistance.parse_callback_data",
            new=Mock(return_value=(new_question_type, 1)),
        ),
    ):
        await select_assistance(update, context)

    assert context.user_data[States.GET_USERNAME] == expected_type_saved, (
        f"Handler must {(not new_question_type and 'not ')}"
        f"save question type in context.user_data if it "
        f"is{(not new_question_type and ' not')} valid"
    )


@pytest.mark.parametrize(
    "keyboard_markup, should_call_edit_message_text",
    [
        (json.dumps(dict()), False),
        (json.dumps(dict(changed=True)), True),
    ],
)
@pytest.mark.asyncio
async def test_select_assistance_change_reply_markup_if_updated(
    update, keyboard_markup, should_call_edit_message_text
):
    """Select assistance handler change reply markup unittest."""
    update.callback_query.message.reply_markup.to_json = Mock(
        return_value=json.dumps(dict())
    )
    context = common_settings["context"]
    context.user_data = common_settings["user_data"]
    keyboard = common_settings["keyboard"]
    keyboard.markup = keyboard_markup
    with (
        patch(
            "bot.handlers.assistance.build_question_keyboard",
            new=AsyncMock(return_value=keyboard),
        ),
        patch(
            "bot.handlers.assistance.parse_callback_data",
            new=Mock(return_value=(None, None)),
        ),
    ):
        await select_assistance(update, context)

    if should_call_edit_message_text:
        update.callback_query.edit_message_text.assert_called_once_with(
            text=SELECT_QUESTION,
            reply_markup=keyboard.markup,
        )
    else:
        update.callback_query.edit_message_text.assert_not_called()
