import pytest

from bot.constants.messages import ASSISTANCE_TYPE_MESSAGE
from bot.constants.states import States
from bot.handlers.assistance import select_type_of_help
from bot.keyboards.assistance_types import assistance_types_keyboard_markup


@pytest.mark.asyncio
async def test_select_type_of_help_response(update, context):
    """Receive select type of help handler returns correct response unittest."""
    response = await select_type_of_help(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=assistance_types_keyboard_markup,
    )
    assert response == States.ASSISTANCE_TYPE, (
        f"Invalid state value,  should be {States.ASSISTANCE_TYPE}",
    )


common_settings = {
    "region": "Test_region",
    "keyboard_markup": assistance_types_keyboard_markup,
}


@pytest.mark.parametrize(
    "region, initial_region, expected_region_changed",
    [
        ("Test_region", "Another_test_region", True),
        (States.ASSISTANCE_TYPE.value, "Test_region", False),
    ],
)
@pytest.mark.asyncio
async def test_select_type_of_help_store_region(
    update, context, region, initial_region, expected_region_changed
):
    """Receive select type of help handler stores correct region in context unittest."""
    update.callback_query.data = region
    context.user_data = {States.REGION: initial_region}

    await select_type_of_help(update, context)

    update.callback_query.answer.assert_called_once()
    update.callback_query.edit_message_text.assert_called_once_with(
        text=ASSISTANCE_TYPE_MESSAGE,
        reply_markup=common_settings["keyboard_markup"],
    )
    assert (
        context.user_data[States.REGION] == region
    ) == expected_region_changed, (
        f"Region in context.user_data must"
        f"{(not expected_region_changed and ' not')} "
        f"be changed, if States.ASSISTANCE_TYPE in callback_query.data."
    )
