from sqlalchemy import Integer, Column, DateTime, String, func, ForeignKey, Boolean, Enum, create_engine
from sqlalchemy.orm import declarative_base, relation, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    def __repr__(self):
        return f"Player(username={self.username})"

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    player_1_id = Column(Integer, ForeignKey("players.id"))
    player_2_id = Column(Integer, ForeignKey("players.id"))

    started_at = Column(DateTime, server_default=func.now(), nullable=False)
    ended_at = Column(DateTime, nullable=True)

    player_1 = relation("Player", foreign_keys=[player_1_id])
    player_2 = relation("Player", foreign_keys=[player_2_id])

class Piece(Base):
    __tablename__ = 'pieces'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    color = Column(Enum("black", "white"))
    type = Column(Enum("pawn", "bishop", "knight", "king", "queen", "rook"))
    row = Column(Integer)
    column = Column(Integer)
    captured = Column(Boolean, default=False)

    game = relation("Game", back_populates="pieces")

Game.pieces = relation("Piece", back_populates="game")

class Move(Base):
    __tablename__ = 'moves'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id"))

    piece_id = Column(Integer, ForeignKey("pieces.id"))
    type = Column(Enum('normal', 'en-passant', 'castling', 'promotion'))

    from_row = Column(Integer)
    from_col = Column(Integer)
    to_row = Column(Integer)
    to_col = Column(Integer)

    capture = Column(Boolean)
    captured_piece = Column(Enum("pawn", "bishop", "knight", "king", "queen", "rook"))
    promotes_to = Column(Enum("pawn", "bishop", "knight", "king", "queen", "rook"))

    piece = relation("Piece")
    game = relation("Game", back_populates="history")

Game.history = relation("Move", back_populates="game")

Base.metadata.create_all(engine)
