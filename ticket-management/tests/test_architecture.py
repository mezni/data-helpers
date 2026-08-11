from pathlib import Path


def test_required_modules_exist() -> None:
    modules = [
        "auth",
        "users",
        "tickets",
        "comments",
        "attachments",
        "health",
    ]

    for module in modules:
        assert (Path("app") / module).is_dir()


def test_business_module_layers_exist() -> None:
    modules = [
        "auth",
        "users",
        "tickets",
        "comments",
        "attachments",
    ]

    for module in modules:
        module_path = Path("app") / module

        assert (module_path / "router.py").exists()
        assert (module_path / "schemas.py").exists()
        assert (module_path / "service.py").exists()
        assert (module_path / "repository.py").exists()


def test_common_modules_exist() -> None:
    assert Path("app/common").is_dir()
    assert Path("app/core").is_dir()


def test_main_application_exists() -> None:
    assert Path("app/main.py").exists()
