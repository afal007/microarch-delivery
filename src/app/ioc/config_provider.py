from dynaconf import Dynaconf
from dishka import Provider, provide, Scope


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def get_config(self) -> Dynaconf:
        return Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=['settings.toml', '.secrets.toml'],
            environments=True,
            merge_enabled=True,
        )
