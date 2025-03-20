<script setup lang="ts">
import { TheChessboard } from "vue3-chessboard";
import "vue3-chessboard/style.css";
import type { BoardApi, BoardConfig } from "vue3-chessboard";
import { useChatStore } from "../stores/chatStore";
import { Mistral } from "@mistralai/mistralai";
import { Chess } from "chess.js";
import { ref, onMounted } from "vue";

let boardAPI: BoardApi;
const boardConfig: BoardConfig = {
  coordinates: true,
};

const chatStore = useChatStore();

function handleCheckmate(isMated: string) {
  if (isMated === "w") {
    alert("Black wins!");
  } else {
    alert("White wins!");
  }
}

function displayBoard(pgn) {
  /* 
  Exemple of result : 

    +-----------------+
  8 | R N B Q K B . R |
  7 | P P P P P P P P |
  6 | . . . . . N . . |
  5 | . . . . . . . . |
  4 | . . . P . . . . |
  3 | . . N . . . . . |
  2 | P P P . P P P P |
  1 | R . B Q K B N R |
    +-----------------+
      a b c d e f g h  
 */

  const chess = new Chess();
  chess.loadPgn(pgn); // Load the PGN

  const board = chess.board(); // Get board as a 2D array

  let boardStr = "  +-----------------+\n";
  for (let i = 0; i <= 7; i++) {
    let row = `${8 - i} | `;
    for (let j = 0; j < 8; j++) {
      row += board[i][j] ? board[i][j].type.toUpperCase() + " " : ". ";
    }
    boardStr += row + "|\n";
  }
  boardStr += "  +-----------------+\n";
  boardStr += "    a b c d e f g h  ";

  return boardStr;
}

function getLegalNextMoves(pgn) {
  const chess = new Chess();
  chess.loadPgn(pgn); // Load the current game state from PGN

  const moves = chess.moves(); // Get all legal moves in SAN notation
  return moves;
}

async function mistralMovePrediction(
  nextMovePossible: string,
  pgn: string,
  impossibleMoves: Array<string>
): Promise<string> {
  const apiKey = import.meta.env.VITE_MISTRAL_API_KEY;
  const client = new Mistral({ apiKey: apiKey });
  var prompt = `You can answer only one of the moves in the following list: \n ${nextMovePossible}\n\nCurrent game in PGN format: ${pgn}\n\nWhat is your next move?\n`;

  if (impossibleMoves.length != 0) {
    for (var impossibleMove in impossibleMoves) {
      prompt += `You cannot play ${impossibleMoves[impossibleMove]}\n`;
    }
  }

  console.log(prompt);
  const chatResponse = await client.chat.complete({
    model: "mistral-large-latest",
    messages: [
      {
        role: "system",
        content:
          "Answer ONLY with the next move in SAN format.\n\nExample :\nc4\n\nOther example :\nO-O",
      },
      {
        role: "user",
        content: prompt,
      },
    ],
  });

  console.log(chatResponse.choices[0].message.content);

  return chatResponse.choices[0].message.content;
}

async function handleMove(move) {
  var pgn = boardAPI.getPgn();

  const nextMovePossible = getLegalNextMoves(pgn);

  if (move.color === "w") {
    chatStore.addUserMessage(move.san);

    if (nextMovePossible.length != 0) {
      var validMove = false;
      var impossibleMoves = [];
      var attempts = 0; // Add counter variable
      var maxAttempts = 5; // Maximum number of attempts

      console.log(displayBoard(pgn));

      while (validMove == false && attempts < maxAttempts) {
        var movePrediction = await mistralMovePrediction(
          nextMovePossible.join(", "),
          pgn,
          impossibleMoves
        );
        validMove = boardAPI.move(movePrediction);
        attempts++; // Increment counter

        if (validMove == false) {
          console.log("Invalid move : " + movePrediction);
          impossibleMoves.push(movePrediction);
        }

        // Cooldown of 1 second
        await new Promise((resolve) => setTimeout(resolve, 2000));
      }

      // Optional: Handle the case when maximum attempts are reached
      if (!validMove) {
        console.log(
          "Reached maximum attempts (" +
            maxAttempts +
            "). Could not find valid move."
        );
        alert("AI give up, 5 attempts reached. You win!");
      }
    } else {
      console.log("No possible moves left.");
    }
  } else {
    chatStore.addOtherMessage("user2", "Mistral AI", move.san);
  }
}
</script>

<template>
  <section>
    <div>
      <button @click="boardAPI?.toggleOrientation()">Toggle orientation</button>
      <button @click="boardAPI?.resetBoard()">Reset</button>
      <button @click="boardAPI?.undoLastMove()">Undo</button>
      <button @click="boardAPI?.toggleMoves()">Threats</button>
    </div>
    <TheChessboard
      :board-config="boardConfig"
      @board-created="(api) => (boardAPI = api)"
      @checkmate="handleCheckmate"
      @move="handleMove"
    />
  </section>
</template>
