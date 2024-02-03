# OHM Model

## Overview

The OHM model is an agent-based simulation designed to model a staking token economy. It simulates the behavior of stakers, validators, and the economic dynamics of the token supply over time.

## Model Components

### Staker

- **Attributes:**
  - `holding`: Amount of tokens held by the staker.

- **Methods:**
  - `setup()`: Initialize staker attributes.
  - `stake(amount)`: Stake a certain amount of tokens.
  - `unstake(amount)`: Unstake a certain amount of tokens.

### Validator

- **Attributes:**
  - `operational_cost`: Operational cost incurred by the validator.
  - `performance`: Placeholder for validator performance.

- **Methods:**
  - `setup()`: Initialize validator attributes.
  - `validate()`: Placeholder validation logic.

### OHM Model

- **Parameters:**
  - `initial_supply`: Initial supply of tokens.
  - `yearly_emissions`: Yearly emissions rate for the first decade.
  - `validator_incentives`: Validator incentives rate.
  - `treasury_emissions`: Treasury emissions rate.
  - `transaction_rate_L1`: Transaction rate on Layer 1.
  - `transaction_rate_middleware`: Transaction rate on middleware.
  - `transaction_fee_L1`: Transaction fee on Layer 1.
  - `transaction_fee_middleware`: Transaction fee on middleware.
  - `num_validators_L1`: Number of validators on Layer 1.
  - `num_validators_middleware`: Number of validators on middleware.
  - `operational_cost_per_validator`: Operational cost per validator.
  - `staking_provision`: Staking provision rate.
  - `economic_outlook_scenarios`: List of economic outlook scenarios (e.g., 'bull', 'base', 'bear').
  - `incentivization_scenarios`: List of incentivization scenarios (e.g., 'scenario1', 'scenario2', 'scenario3').
  - `adoption_scenarios`: List of adoption scenarios (e.g., 'low', 'medium', 'high').
  - `simulation_duration`: Duration of the simulation in years.

- **Model Components:**
  - `stakers`: AgentList of Staker agents.
  - `validators_L1`: AgentList of Validator agents for Layer 1.
  - `validators_middleware`: AgentList of Validator agents for middleware.
  - `treasury`: Treasury to store rewards.
  - `total_supply`: Total token supply.

- **Methods:**
  - `setup()`: Initialize model parameters and components.
  - `step()`: Perform model steps, including staker and validator behaviors.
  - `calculate_total_supply()`: Calculate the total token supply.

## Usage

1. **Run Model:**
   ```bash
   docker-compose up

   
   Visit http://127.0.0.1:8000 in your browser.

## Acknowledgments
This model uses the agentpy library for agent-based modeling.
Reference : https://github.com/chadury2021/agentpy/tree/master
