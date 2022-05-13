"""Test the Raspberry Pi hardware platform."""
from homeassistant.components.hassio import DATA_OS_INFO
from homeassistant.components.raspberrypi.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from tests.common import MockModule, mock_integration


async def test_board_info(hass: HomeAssistant, hass_ws_client) -> None:
    """Test we can get the board info."""
    mock_integration(hass, MockModule("hassio"))
    hass.data[DATA_OS_INFO] = {"board": "rpi"}

    assert await async_setup_component(hass, DOMAIN, {})

    client = await hass_ws_client(hass)

    await client.send_json({"id": 1, "type": "hardware/info"})
    msg = await client.receive_json()

    assert msg["id"] == 1
    assert msg["success"]
    assert msg["result"] == {
        "hardware": [
            {
                "image": "https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg",
                "name": "Raspberry Pi",
                "type": "board",
                "url": "https://theuselessweb.com/",
            }
        ]
    }
