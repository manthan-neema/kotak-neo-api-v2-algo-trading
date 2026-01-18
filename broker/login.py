from config.session_store import save_session, load_session
from neo_api_client import NeoAPI
from config.env import CONSUMER_KEY, MOBILE, UCC, MPIN, validate_env


def _validate_token_response(resp, step_name):
    if not isinstance(resp, dict):
        raise RuntimeError(f"{step_name} returned invalid response: {resp}")

    data = resp.get("data")
    if not data or "token" not in data:
        raise RuntimeError(f"{step_name} failed. Response: {resp}")

    return data


def get_new_client():
    validate_env()

    client = NeoAPI(
        environment="prod",
        consumer_key=CONSUMER_KEY,
    )
    print("Client initialized")

    # ---- STEP 1: TOTP LOGIN ----
    totp = input("Enter current TOTP from authenticator app: ").strip()
    print("Calling TOTP login...")

    resp_login = client.totp_login(
        mobile_number=MOBILE,
        ucc=UCC,
        totp=totp
    )
    _validate_token_response(resp_login, "TOTP login")
    print("TOTP login OK")

    # ---- STEP 2: MPIN VALIDATION ----
    print("Validating MPIN...")
    resp_validate = client.totp_validate(mpin=MPIN)
    data = _validate_token_response(resp_validate, "MPIN validation")

    save_session(resp_validate)
    print("✅ Login successful")
    return client


def get_cache_stored_client():
    session = load_session()
    if not session or "data" not in session:
        return get_new_client()

    data = session["data"]

    if "token" not in data:
        return get_new_client()

    client = NeoAPI(
        environment="prod",
        consumer_key=CONSUMER_KEY,
        access_token=data["token"],
    )

    cfg = client.api_client.configuration
    cfg.edit_token = data.get("token")
    cfg.edit_sid = data.get("sid")
    cfg.edit_rid = data.get("rid")
    cfg.serverId = data.get("hsServerId")
    cfg.data_center = data.get("dataCenter")
    cfg.base_url = data.get("baseUrl")

    return client


def get_authenticated_client():
    client = get_cache_stored_client()

    try:
        response = client.positions()

        if not response or response.get("stCode") != 200:
            raise RuntimeError(f"Session validation failed: {response}")

        print("✅ Loaded session from store")
        return client

    except Exception as e:
        print(f"❌ Stored session invalid: {e}")
        return get_new_client()