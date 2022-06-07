// window.onload = function() {
//         let things = document.getElementsByTagName("input")
//         const inputs = Array.from(things)
//         inputs.forEach(input => {
//                 input.addEventListener('keypress', () => {
//                        if(input.readOnly == true){
//                                alert("This is a readonly field")
//                        }
//                 })
//         })
//       };



function toggle(source) {
        checkboxes = document.getElementsByName('foo');
        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = source.checked;
        }
      }



const loadTotal = () => {
        let outstanding_bill = document.getElementById('outstanding_bill')
        let amount = document.getElementById('total_amount_due')
        let expiration_bill = document.getElementById('expiration_bill')
        let renewal_bill = document.getElementById('renewal_bill')

        var testExp = !!document.getElementById("expiration_bill");
        var testRen = !!document.getElementById("renewal_bill");        

        if(testExp === true && testRen === true ){
                amount.value = expiration_bill.value + renewal_bill.value       
        }
        else{
                amount.value = outstanding_bill.value
        }
        

}



const findArrears = () => {
        let total = document.getElementById('total_amount_due')
        let amount = document.getElementById('amount_paid')
        let arrears = document.getElementById('arrears')

        arrears.value = total.value - amount.value

}

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



const radioCheck = () => {
        for(let i=1; i<5; i++){
                let radio = document.getElementById("install"+i)
                let period = document.getElementById("period")
                let set_date =   document.getElementById("set_pay_date")

                if(radio.checked){
                        amount.disabled = false 

                        if(radio.value == "None"){
                                period.disabled = true    
                                set_date.disabled = false 

                        }
                        else{
                                period.placeholder = `Enter the number of ${radio.value}` 
                                period.disabled = false    
                                set_date.disabled = true 

                               
                        }
                }
                }
} 


const checkDate = () => {

        let check = document.getElementById('check')

        if(check.checked == true){
                document.getElementById("start_date").disabled = false
                document.getElementById("end_date").disabled = false
        }else{
                document.getElementById("start_date").disabled = true
                document.getElementById("end_date").disabled = true 
        }
}






// const getValue = () => {
//         $('#{values}').on("change", function() {

//                 $('.data').each(function() {
//                   alert($(this).val())
                 
//                 });
                
//               });
//                 $(".data").on("change", function() {
              
//                 $('.data').each(function() {
//                   alert($(this).val())
                 
//                 });
                
//               }); 
// }
//         // $(document).ready(function(){
        //         $("button").click(function(){
        //           $("p").slideToggle();
        //         });
        //       });

//                 // Fee Items
// $("#fee_type").change(function () {
//                 var url = $("#myFormID").attr("data-items-url");
//                 var fee_type = $(this).val();
            
//                 $.ajax({
//                   url: url,
//                   data: {
//                     'fee_type': fee_type,
//                   },
//                   success: function (data) {
//                     $("#fee_items").html(data);
//                   }
//                 });
            
//         });  
        


       