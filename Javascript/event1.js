function filterGifts(gifts) {
  return [gifts != "#"];
}

let regalos = ["#gameboy", "Gamecube", "Nds"];

const resultado = regalos.filter((regalo) => !regalo.includes("#"));
console.log(resultado);

function filterGifts(gifts) {
  // Code here
  if (gifts.length === "") {
    console.log("el array no puede estar vacio");
    return [];
  }

  const filtro = gifts.filter((gift) => !gift.includes("#"));
  console.log(filtro);
  return filtro;
}

filterGifts(["D#si", "3DS"]);
