from twip import dir
from twip.extension.connector import Connector, ConnectorSide

import tt


def test_connector_touches_room():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    assert connector.touches(tt.ROOM_1)
    assert connector.touches(tt.ROOM_2)


def test_connector_does_not_touch_unconnected_room():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    assert not connector.touches(tt.ROOM_3)


def test_connector_returns_side_for_room():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    side = connector.side_for(tt.ROOM_1)

    assert side is not None
    assert side.room == tt.ROOM_1
    assert side.traits == {dir.N}


def test_connector_returns_none_for_missing_side():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    assert connector.side_for(tt.ROOM_3) is None


def test_connector_returns_other_side():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    side = connector.other_side(tt.ROOM_1)

    assert side is not None
    assert side.room == tt.ROOM_2
    assert side.traits == {dir.S}


def test_connector_returns_none_for_other_side_when_room_missing():
    connector = Connector(
        sides=(
            ConnectorSide(room=tt.ROOM_1, traits={dir.N}),
            ConnectorSide(room=tt.ROOM_2, traits={dir.S}),
        )
    )

    assert connector.other_side(tt.ROOM_3) is None