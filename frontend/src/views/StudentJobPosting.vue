<template>

<div class="container mt-4">

    <h2>{{ job.title }}</h2>

    <div class="card mt-3">

        <div class="card-header">

            Job Details

        </div>

        <div class="card-body">

            <table class="table">

                <tr>
                    <th width="220">Company</th>
                    <td>{{ job.company_name }}</td>
                </tr>

                <tr>
                    <th>Description</th>
                    <td>{{ job.description || "NA" }}</td>
                </tr>

                <tr>
                    <th>Package</th>
                    <td>{{ job.salary || "Not Disclosed" }}</td>
                </tr>

                <tr>
                    <th>Minimum CGPA</th>
                    <td>{{ job.min_cgpa || "Not Required" }}</td>
                </tr>

                <tr>
                    <th>Skills</th>
                    <td>{{ job.skills_required || "NA" }}</td>
                </tr>

                <tr>
                    <th>Location</th>
                    <td>{{ job.job_location || "NA" }}</td>
                </tr>

                <tr>
                    <th>Vacancies</th>
                    <td>{{ job.vacancies }}</td>
                </tr>

                <tr>
                    <th>Deadline</th>
                    <td>{{ formatDate(job.deadline) }}</td>
                </tr>

            </table>

            <button
                class="btn btn-success"
                @click="applyJob"
                :disabled="job.already_applied">

                {{ job.already_applied ? "Already Applied" : "Apply" }}

            </button>

        </div>

    </div>

</div>

</template>

<script>

import axios from "axios"

export default{

    data(){

        return{

            job:{}

        }

    },

    async mounted(){

        await this.loadJob()

    },

    methods:{

        async loadJob(){

            const response = await axios.get(

                `http://127.0.0.1:5000/student/job_posting/${this.$route.params.id}`,

                {
                    headers:{
                        Authorization:`Bearer ${localStorage.getItem("token")}`
                    }
                }

            )

            this.job=response.data

        },

        async applyJob(){

            const response = await axios.post(

                `http://127.0.0.1:5000/student/job_posting/${this.job.id}/apply`,

                {},

                {
                    headers:{
                        Authorization:`Bearer ${localStorage.getItem("token")}`
                    }
                }

            )

            alert(response.data.message)

            await this.loadJob()

        },

        formatDate(date){

            return new Date(date).toLocaleString("en-GB")

        }

    }

}

</script>