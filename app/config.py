import os

from omegaconf import OmegaConf


class Config:
    _instance = None
    default_config = {
        "server": {
            "name": "HomuraMC",
            "ip": "0.0.0.0",
            "port": 25565,
            "max_players": 20,
            "motd": "A HomuraMC server",
            "online_mode": True,
        }
    }

    def __new__(cls, file_path="homura.yml"):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config = cls.load_config(file_path)
        return cls._instance

    @classmethod
    def load_config(cls, file_path):
        if not os.path.exists(file_path):
            cls.write_default_config(file_path)
        config = OmegaConf.load(file_path)
        return config

    @classmethod
    def write_default_config(cls, file_path):
        default_conf = OmegaConf.create(cls.default_config)
        with open(file_path, "w") as f:
            OmegaConf.save(config=default_conf, f=f.name)