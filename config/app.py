from omegaconf import DictConfig, OmegaConf

import hydra


# @hydra.main(config_path="config", config_name="config")
@hydra.main(config_name="config")
def app(cfg: DictConfig) -> None:
    # conf = OmegaConf.create({"k": "v", "list": [1, {"a": "1", "b": "2", 3: "c"}]})
    # print(OmegaConf.to_yaml(conf))
    result = hydra.utils.instantiate(cfg.db.sumsub)
    # result = hydra.utils.instantiate(cfg.db)
    print(result)
    x = result.add()
    print(x)

    md = hydra.utils.instantiate(cfg.dir2.muldiv)
    print(md)
    y = md.multiply()
    print(y)


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
