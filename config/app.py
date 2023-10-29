from omegaconf import DictConfig
import hydra


# @hydra.main(config_path="config", config_name="config")
@hydra.main(config_name="config")
def app(cfg: DictConfig) -> None:
    result = hydra.utils.instantiate(cfg.db.sumsub)
    # result = hydra.utils.instantiate(cfg.db)
    x = result.add()
    print(x)


if __name__ == "__main__":
    app()

# import hydra
# from omegaconf import DictConfig, OmegaConf
# @hydra.main(config_name="config")
# def app(cfg: DictConfig) -> None:
#     print(OmegaConf.to_yaml(cfg))
#
#
# if __name__ == "__main__":
#     app()
