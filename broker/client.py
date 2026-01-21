import os
import tkinter as tk
from tkinter import simpledialog
from dotenv import load_dotenv
from config.session_store import save_session, load_session
from neo_api_client import NeoAPI


class Client:
    _instance = None

    def __init__(self):
        load_dotenv()
        self._CONSUMER_KEY = os.getenv("KOTAK_CONSUMER_KEY")
        self._MOBILE = os.getenv("KOTAK_MOBILE")
        self._UCC = os.getenv("KOTAK_UCC")
        self._MPIN = os.getenv("KOTAK_MPIN")
        self._client = None
        self._token = None
        self._sid = None
        self._baseurl=None
        self._validate_env()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
        return cls._instance

    def get_client(self):
        if self._client is None:
            self._client = self._get_authenticated_client()
        return self._client

    def _validate_token_response(self, resp, step_name):
        if not isinstance(resp, dict):
            raise RuntimeError(f"{step_name} returned invalid response: {resp}")

        data = resp.get("data")
        if not data or "token" not in data:
            raise RuntimeError(f"{step_name} failed. Response: {resp}")

        return data

    def _validate_env(self):
        required = {
            "KOTAK_CONSUMER_KEY": self._CONSUMER_KEY,
            "KOTAK_MOBILE": self._MOBILE,
            "KOTAK_UCC": self._UCC,
            "KOTAK_MPIN": self._MPIN,
        }

        missing = [k for k, v in required.items() if not v]
        if missing:
            raise RuntimeError(f"Missing env vars: {missing}")

    def _get_new_client(self):
        client = NeoAPI(
            environment="prod",
            consumer_key=self._CONSUMER_KEY,
        )
        print("Client initialized")

        # ---- STEP 1: TOTP LOGIN ----
        root = tk.Tk()
        root.withdraw()

        totp = simpledialog.askinteger("Input", "Enter current TOTP from authenticator app:")

        if totp is None:
            raise RuntimeError("TOTP entry cancelled by user")
        print("Calling TOTP login...")
        resp_login = client.totp_login(
            mobile_number=self._MOBILE,
            ucc=self._UCC,
            totp=str(totp).strip()
        )
        self._validate_token_response(resp_login, "TOTP login")
        print("TOTP login OK")

        # ---- STEP 2: MPIN VALIDATION ----
        print("Validating MPIN...")
        resp_validate = client.totp_validate(mpin=self._MPIN)
        data = self._validate_token_response(resp_validate, "MPIN validation")

        save_session(resp_validate)
        print("✅ Login successful")
        return client

    def _get_cache_stored_client(self):
        session = load_session()
        if not session or "data" not in session:
            return self._get_new_client()

        data = session["data"]

        if "token" not in data:
            return self._get_new_client()

        client = NeoAPI(
            environment="prod",
            consumer_key=self._CONSUMER_KEY,
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

    def _get_authenticated_client(self):
        client = self._get_cache_stored_client()

        try:
            response = client.positions()

            if not response or response.get("stCode") != 200:
                raise RuntimeError(f"Session validation failed: {response}")

            print("✅ Loaded session from store")
            return client

        except Exception as e:
            print(f"❌ Stored session invalid: {e}")
            client=self._get_new_client()
            return client

