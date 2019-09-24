import numpy as np

# global stopping criteria
EPS = 0.001

def value_iteration(model, maxiter=100):

    # initialize the value function and policy
    pi = np.ones((model.num_states, 1))
    val_ = np.zeros((model.num_states, 1))

    for i in range(maxiter):
        # initialize delta
        delta = 0
        # perform Bellman update for each state
        for state in range(model.num_states):
            # store old value
            tmp = val_[state].copy()
            # compute the value function
            val_[state] = np.max( np.sum((model.R[state] + model.gamma * val_) * model.P[state,:,:], 0) )
            # find maximum change in value
            delta = np.max( (delta, np.abs(tmp - val_[state])) )
        # stopping criteria
        if delta <= EPS * (1 - model.gamma) / model.gamma:
            print("Stopped after %d iterations." %  i)
            break
    # compute the policy
    for state in range(model.num_states):
        pi[state] = np.argmax(np.sum(val_ * model.P[state,:,:],0))

    return val_, pi

def policy_iteration(model, maxiter):
    # initialize the value function and policy
    pi = np.ones((model.num_states, 1))
    val_ = np.zeros((model.num_states, 1))

    for i in range(maxiter):
        # Stopping criteria
        stable_policy = True
        # Policy evaluation
        val_ = policy_evaluation(model, val_, pi)

        for state in range(model.num_states):
            # do policy improvement
            action = np.argmax( np.sum( (model.R[state] + model.gamma * val_) * model.P[state,:,:], 0) )
            # check if policy has been updated
            if action != pi[state]:
                # store new action
                pi[state] = action
                # update stopping criteria
                stable_policy = False

        # check if stopping criteria satisfied
        if stable_policy:
            print("Stopped after %d iterations." % i)
            break

    return val_, pi

def policy_evaluation(model, val_, policy):
    loop = True
    while loop:
        # initialize delta
        delta = 0
        for state in range(model.num_states):
            # store old value
            tmp = val_[state].copy()
            # compute the value function
            val_[state] = np.sum( (model.R[state] + model.gamma * val_) * model.P[state,:,int(policy[state])].reshape(-1,1))
            # find maximum change in value
            delta = np.max( (delta, np.abs(tmp - val_[state])) )
        # stopping criteria
        if delta <= EPS * (1 - model.gamma) / model.gamma:
            loop = False

    return val_