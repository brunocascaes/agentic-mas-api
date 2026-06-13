from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, ForeignKeyConstraint, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy import func

Base = declarative_base()

class Simulation(Base):
    __tablename__ = "simulations"

    simulation_id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(Text, nullable=False)
    attributes = Column(JSONB)
    metrics = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True))


class Round(Base):
    __tablename__ = "rounds"

    simulation_id = Column(Integer, ForeignKey("simulations.simulation_id"), primary_key=True)
    round_id = Column(Integer, primary_key=True)
    attributes = Column(JSONB)
    metrics = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True))


class Agent(Base):
    __tablename__ = "agents"

    simulation_id = Column(Integer, ForeignKey("simulations.simulation_id"), primary_key=True)
    agent_id = Column(Integer, primary_key=True)
    attributes = Column(JSONB)
    state = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())


class Decision(Base):
    __tablename__ = "decisions"

    decision_id = Column(Integer, primary_key=True, autoincrement=True)
    simulation_id = Column(Integer, nullable=False)
    round_id = Column(Integer, nullable=False)
    agent_id = Column(Integer, nullable=False)
    framework = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    config = Column(JSONB)
    context = Column(JSONB)
    response = Column(JSONB)
    status = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    finished_at = Column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["simulation_id", "agent_id"],
            ["agents.simulation_id", "agents.agent_id"]
        ),
        ForeignKeyConstraint(
            ["simulation_id", "round_id"],
            ["rounds.simulation_id", "rounds.round_id"]
        ),
        Index("idx_decision_sim_agent", "simulation_id", "agent_id"),
        Index("idx_decision_sim_round", "simulation_id", "round_id"),
    )
