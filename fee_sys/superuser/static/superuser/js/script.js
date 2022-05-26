const checkFunction = () => {
        for(let i=1; i<10; i++){
                    let checkBox = document.getElementById("fee_type"+i)
                    let amount = document.getElementById("item_amount"+i)

            if (checkBox.checked == true) {
                    amount.style.display = "block"
            } else {
                    amount.style.display = "none";
                }
            }
        }