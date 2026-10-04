document.addEventListener("DOMContentLoaded", function () {

    // ================= FEE SELECTION =================

    window.selectFee = function (gender) {

        const genderSelect = document.getElementById("gender");
        const feeInput = document.getElementById("fee");
        const form = document.getElementById("registrationForm");

        if (genderSelect) {
            genderSelect.value = gender;
        }

        if (feeInput) {

            if (gender === "Girls") {
                feeInput.value = "₹2400";
            }

            if (gender === "Boys") {
                feeInput.value = "₹2800";
            }
        }

        if (form) {
            form.scrollIntoView({
                behavior: "smooth"
            });
        }
    };


    // ================= GENDER =================

    const gender = document.getElementById("gender");
    const fee = document.getElementById("fee");

    if (gender) {

        gender.addEventListener("change", function () {

            if (this.value === "Girls") {

                fee.value = "₹2400";

            } else if (this.value === "Boys") {

                fee.value = "₹2800";

            } else {

                fee.value = "";
            }

        });
    }


    // ================= REGISTRATION =================

    const registrationForm =
        document.getElementById("registrationForm");


    if (registrationForm) {

        registrationForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();

                console.log("Register button clicked");


                const name =
                    document.getElementById("name").value.trim();

                const mobile =
                    document.getElementById("mobile").value.trim();

                const selectedGender =
                    document.getElementById("gender").value;


                console.log("Name:", name);
                console.log("Mobile:", mobile);
                console.log("Gender:", selectedGender);


                // Mobile validation

                if (!/^[0-9]{10}$/.test(mobile)) {

                    alert(
                        "Please enter valid 10 digit mobile number."
                    );

                    return;
                }


                // Gender validation

                if (selectedGender === "") {

                    alert("Please select gender.");

                    return;
                }


                // Data sent to FastAPI

                const studentData = {

                    name: name,

                    mobile: mobile,

                    gender: selectedGender

                };


                console.log(
                    "Sending data:",
                    studentData
                );


                try {

                    const response = await fetch(
                        "http://127.0.0.1:8000/register",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type": "application/json"
                            },

                            body: JSON.stringify(studentData)
                        }
                    );


                    console.log(
                        "Response status:",
                        response.status
                    );


                    const data =
                        await response.json();


                    console.log(
                        "Backend response:",
                        data
                    );


                    if (response.ok && data.success) {

                        alert(
                            "Registration Successful!\n\n" +

                            "Name: " +
                            data.name +

                            "\nGender: " +
                            data.gender +

                            "\nMonthly Fee: ₹" +
                            data.fee
                        );


                        registrationForm.reset();

                        document.getElementById("fee").value = "";

                    }

                    else {

                        alert(
                            data.message ||
                            "Registration Failed!"
                        );

                    }

                }

                catch (error) {

                    console.error(
                        "Error:",
                        error
                    );

                    alert(
                        "Backend connection failed!\n\n" +
                        "Please make sure FastAPI is running."
                    );

                }

            }
        );
    }

});