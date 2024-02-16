import agentpy as ap

class Staker(ap.Agent):
    def setup(self, initial_supply, staking_provision):
        self.holding = initial_supply * 0.35
        self.staking_provision = 0.35
        self.staking_rewards = 0  # To track staking rewards
        self.unstaked_amount = 0  # To track unstaking amounts
        self.staked_amount = 0  # To track staked amounts

    def stake(self, amount):
        self.holding += amount
        self.staked_amount += amount
        self.staking_rewards += amount * self.staking_provision

    def unstake(self, amount):
        if self.holding >= amount:
            self.holding -= amount
            self.unstaked_amount += amount
            return amount
        return 0


class Validator(ap.Agent):
    def setup(self):
        self.operational_cost = 10000
        self.performance = 1.0
        self.validator_incentives = 0.02 

    def validate(self):
        # Placeholder validation logic
        return self.performance
    

class OHM(ap.Model):
    def setup(self):
        # Initialize an attribute with parameter requirements
        self.initial_supply = 21e9
        self.yearly_emissions = 0.04  # 4% for the first decade
        self.validator_incentives = 0.02
        self.community_treasury = 0.02
        self.num_validators_L1 = 100
        self.num_validators_middleware = 20
        self.operational_cost_per_validator = 10000
        self.staking_provision = 0.35
        self.incentivization_scenarios = ['scenario1', 'scenario2', 'scenario3']
        self.adoption_scenarios = ['low', 'medium', 'high']
        self.current_step = 0

        # Model components
        self.stakers = ap.AgentList(self, 100, Staker, initial_supply=self.initial_supply, staking_provision=self.staking_provision)
        self.validators_L1 = ap.AgentList(self, self.num_validators_L1, Validator)
        self.validators_middleware = ap.AgentList(self, self.num_validators_middleware, Validator)
        self.treasury = 0
        self.total_supply = self.initial_supply * (1 + self.yearly_emissions)  # Initialize total_supply
        

    def staker_behaviors(self):
        # Staker behaviors
        for staker in self.stakers:
            staking_amount = staker.holding * self.staking_provision
            staker.stake(staking_amount)

            if self.p.economic_outlook_scenarios == 'bull':
                # Adjust parameters for bull market
                staking_reward_increase_percentage = 0.2
                additional_rewards = staker.holding * self.staking_provision * staking_reward_increase_percentage
                staker.stake(additional_rewards)
                staker.staking_provision *= 1.1  # Increase staking rewards

            if self.p.economic_outlook_scenarios == 'bear':
                staker.staking_provision *= 0.8  # Decrease staking rewards
                staker.unstake(0.1 * staker.holding)  # Unstake 10% of holding


    def validator_behaviors(self, validators):
        # Validator behaviors
        for validator in self.validators_L1:
            validation_reward = validator.validate() * self.validator_incentives
            self.treasury += validation_reward
            validator.operational_cost += self.operational_cost_per_validator

            # Additional behaviors in a bull market
            if self.p.economic_outlook_scenarios == 'bull':
                # Adjust parameters for bull market
                validator.validator_incentives *= 1.2  # Increase validation rewards
                validator.operational_cost *= 0.9  # Decrease operational costs
                validator.performance *= 1.1  # Increase performance

            # Additional behaviors in a bear market
            if self.p.economic_outlook_scenarios == 'bear':
                # Adjust parameters for bear market
                validator.validator_incentives *= 0.8  # Decrease validation rewards
                validator.operational_cost *= 1.2  # Increase operational costs
                validator.performance *= 0.9  # Decrease performance


        for validator in self.validators_middleware:
            validation_reward = validator.validate() * self.validator_incentives
            self.treasury += validation_reward
            validator.operational_cost += self.operational_cost_per_validator

            # Additional behaviors in a bull market
            if self.p.economic_outlook_scenarios == 'bull':
                # Adjust parameters for bull market
                validator.validator_incentives *= 1.2  # Increase validation rewards
                validator.operational_cost *= 0.9  # Decrease operational costs
                validator.performance *= 1.1  # Increase performance

            # Additional behaviors in a bear market
            if self.p.economic_outlook_scenarios == 'bear':
                # Adjust parameters for bear market
                validator.validator_incentives *= 0.8  # Decrease validation rewards
                validator.operational_cost *= 1.2  # Increase operational costs
                validator.performance *= 0.9  # Decrease performance

    def step(self):
        print(f"\n Current economic outlook scenarios: {self.p.economic_outlook_scenarios}")

        if self.p.economic_outlook_scenarios == 'bull':
            print('bull')
            self.validator_incentives *= 1.2
            self.community_treasury += 0.02 * self.total_supply
            self.operational_cost_per_validator *= 0.9
            self.transaction_rate_L1 = 0.2
            self.transaction_rate_middleware = 0.1
            self.transaction_fee_L1 = 0.02
            self.transaction_fee_middleware = 0.01
            self.adoption_level = 'high'
            
            self.staker_behaviors()
            self.validator_behaviors(self.validators_L1)
            self.validator_behaviors(self.validators_middleware)

        elif self.p.economic_outlook_scenarios == 'bear':
            print('bear')
            self.validator_incentives *= 0.8
            self.community_treasury += 0.001 * self.total_supply
            self.transaction_rate_L1 = 0.05
            self.transaction_rate_middleware = 0.02
            self.transaction_fee_L1 = 0.005
            self.transaction_fee_middleware = 0.002
            self.adoption_level = 'low'

            self.staker_behaviors()
            self.validator_behaviors(self.validators_L1)
            self.validator_behaviors(self.validators_middleware)

        else:  # Base market condition
            print('base')
            self.validator_incentives *= 0.9
            self.community_treasury += 0.01 * self.total_supply
            self.transaction_rate_L1 = 0.1
            self.transaction_rate_middleware = 0.05
            self.transaction_fee_L1 = 0.01
            self.transaction_fee_middleware = 0.005
            self.adoption_level = 'medium'

            self.staker_behaviors()
            self.validator_behaviors(self.validators_L1)
            self.validator_behaviors(self.validators_middleware)

        yearly_emission = self.total_supply * self.yearly_emissions
        self.total_supply += min(yearly_emission, 0.04 * self.total_supply)

        self.current_step += 1

    def update(self):

        staking_total = sum(staker.holding * self.staking_provision for staker in self.stakers)
        unstaking_total = sum(staker.unstake(0.1 * staker.holding) for staker in self.stakers)  # Assuming 10% unstaking
        stakers_net_supply = staking_total - unstaking_total

        print(f"Stakers total supply: {stakers_net_supply}")
        self.record('Stakers_Net_Supply', stakers_net_supply)


        # Update staking rewards
        total_staking_rewards = sum(staker.staking_rewards for staker in self.stakers)
        self.record('Total_Staking_Rewards', total_staking_rewards)

        # Update unstaking amounts
        total_unstaking_amount = sum(staker.unstaked_amount for staker in self.stakers)
        self.record('Total_Unstaking_Amount', total_unstaking_amount)

        # Calculate and record staking yield
        staking_yield = (total_staking_rewards / staking_total) * 100
        self.record('Staking_Yield', staking_yield)

        # Update staking provisions
        total_staked_amount = sum(staker.staked_amount for staker in self.stakers)
        self.record('Total_Staked_Amount', total_staked_amount)

        validators_total_supply_L1 = sum(validator.operational_cost for validator in self.validators_L1)
        validators_total_supply_middleware = sum(validator.operational_cost for validator in self.validators_middleware)
        print(f"Validators (L1) total supply: {validators_total_supply_L1}")
        self.record('Validators_L1_Total_Supply', validators_total_supply_L1)
        print(f"Validators (Middleware) total supply: {validators_total_supply_middleware}")
        self.record('Validators_Middleware_Total_Supply', validators_total_supply_middleware)

        print(f"Total supply at step {self.current_step}: {self.total_supply}")
        self.record('Total_Supply', self.total_supply)

    