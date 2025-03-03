import pufferlib

# TODO: Fix circular import depending on import order
from clean_pufferl import CleanPuffeRL
import config as demo_config

config = demo_config.NMMO()
#config = demo_config.Atari(framestack=1)
#config = demo_config.MAgent()
#config = demo_config.Griddly()
#config = demo_config.Crafter()
#config = demo_config.NetHack()

all_bindings = [config.all_bindings[0]]

for binding in all_bindings:
    agent = pufferlib.frameworks.cleanrl.make_policy(
            config.Policy, recurrent_args=config.recurrent_args,
            recurrent_kwargs=config.recurrent_kwargs,
        )(binding, *config.policy_args, **config.policy_kwargs).to(config.device)

    trainer = CleanPuffeRL(
            binding,
            agent,
            num_buffers=config.num_buffers,
            num_envs=config.num_envs,
            num_cores=config.num_cores,
            batch_size=config.batch_size,
            vec_backend=config.vec_backend,
            seed=config.seed,
    )

    #trainer.load_model(path)
    #trainer.init_wandb()

    data = trainer.allocate_storage()

    num_updates = config.total_timesteps // config.batch_size
    for update in range(num_updates):
        trainer.evaluate(agent, data)
        trainer.train(agent, data, 
            batch_rows=config.batch_rows,
            bptt_horizon=config.bptt_horizon,
        )

    trainer.close()