User has a Matrix chat room with 8 other participants. Need to check if Matrix connection is configured.
§
Matrix offline issue: had TWO gateway processes running - old one (PID 13059) used different venv without mautrix. Fix: kill all gateway processes and restart to use correct venv with mautrix installed.
§
Matrix config mismatch (2026-05-18): `MATRIX_HOMESERVER=https://matrix.capitaltrain.cn` but `MATRIX_USER_ID=@amber:matrix.git4ta.fun` and `MATRIX_HOME_CHANNEL=!IjMyrStGXBJuVycZVe:matrix.git4ta.fun`. User confirmed capitaltrain.cn is the active server. Need to update USER_ID and HOME_CHANNEL to capitaltrain.cn domain.
§
Matrix grand_council room ID: !DhnyVDOTFtiv8Bkqrq:matrix.capitaltrain.cn (alias: #grand_council:matrix.capitaltrain.cn). Added to free_response_rooms so bot responds without @mention there.