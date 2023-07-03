import { Block, Piece } from "./BoardState";

const useValidateMovement = () => {
  const isAdjacentBlock = (piecePosition: number[], blockPosition: number[]) =>
    Math.abs(blockPosition[0] - piecePosition[0]) +
      Math.abs(blockPosition[1] - piecePosition[1]) <=
    1;

  const isSameBlock = (piecePosition: number[], blockPosition: number[]) =>
    blockPosition[0] === piecePosition[0] &&
    blockPosition[1] === piecePosition[1];

  const isSameOwner = (selectedPiece: Piece, block: Block) =>
    selectedPiece.owner === block.piece?.owner;

  const validateMovement = (selectedPiece: Piece, block: Block) => {
    if (!isAdjacentBlock(selectedPiece.position, block.address)) {
      alert("隣接するマスにしか移動できません");
      return false;
    }
    if (isSameBlock(selectedPiece.position, block.address)) {
      alert("コマを選択中です。同じマスには移動できません");
      return false;
    }
    if (isSameOwner(selectedPiece, block)) {
      alert("自分のコマがあるマスには移動できません");
      return false;
    }
    return true;
  };
  return validateMovement;
};

export default useValidateMovement;
