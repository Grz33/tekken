import numpy as np
import time
from learning_agent import LearningAgent,Screen

TRIAL = 1
TOTAL_TESTS = 1
TOTAL_EPISODES = 1


def save_models(agent, curr_test):
    agent.Model.model.save('Próba1.h5', overwrite=True)
    print("Model saved as: Próba1.h5".format(curr_test))
    agent.learning_agent.Model.target_model.save('próba1Target.h5', overwrite=True)
    print("Target Model saved as: Próbatarget.h5".format(curr_test))


def save_rewards_to_txt(reward_per_episode, file_name="reward.txt"):
    np.savetxt(file_name, reward_per_episode, fmt='%d %.2f %d %d', header="Episode Reward Steps ", comments='')
    print(f"Dane epizodów i nagród zapisane do {file_name}")


def run(agent):
    time.sleep(3)
    screen = Screen.Screen()
    w = screen.get_screen()
    state = np.array([w, w])
    start_time = time.time()
    episode = 0
    true_episode = 0
    curr_test = 1
    record_size = TOTAL_EPISODES * TOTAL_TESTS
    reward_total = 0
    reward_per_episode = np.zeros((record_size, 4))

    i = 0
    try:
        while True:

            screen.get_hp_before_combo()

            action_index = agent.choose_action(state)

            LearningAgent.random_moves.execute(action_index)
            LearningAgent.random_moves.quick_press_delay()
            screen_after_combo = screen.get_screen()

            reward = screen.get_reward()
            print('Nagroda:', reward)
            state_prime = np.array((state[1], screen_after_combo))

            agent.observe((state, action_index, reward, state_prime))
            agent.replay()

            state = state_prime
            reward_total = reward_total + reward

            if time.time() - start_time > 20:
                LearningAgent.random_moves.reset_players()
                time.sleep(2)
                print(true_episode)
                reward_per_episode[i] = [true_episode, reward_total, agent.steps, agent.latest_Q]
                print("Episode {}".format(episode) + " Ended. Reward earned: {}".format(reward_total))

                episode += 1
                true_episode += 1
                i += 1
                start_time = time.time()

            if episode >= TOTAL_EPISODES:
                curr_test += 1
                if curr_test >= TOTAL_TESTS:
                    save_rewards_to_txt(reward_per_episode)

                    save_models(agent, curr_test)
                    break

                else:
                    save_models(agent, curr_test)
                    save_rewards_to_txt(reward_per_episode)
                    curr_test += 1
                    episode = 0
                    start_time = time.time()

    except KeyboardInterrupt:
        reward_per_episode[i] = [episode, reward_total, agent.steps, agent.latest_Q]
        print("Episodes and rewards saved to reward.txt")


def play(agent):
    time.sleep(3)
    screen = Screen.Screen()
    w = screen.get_screen()
    state = np.array([w, w])
    try:
        while True:
            action_index = agent.play(state)
            LearningAgent.random_moves.execute(action_index)
            screen_cap = screen.get_screen()
            state_prime = np.array((state[1], screen_cap))
            state = state_prime

    except KeyboardInterrupt:
        print('break')


if __name__ == '__main__':
    agent = LearningAgent.LearningAgent(learning=True)
    run(agent)
    # play(agent)
