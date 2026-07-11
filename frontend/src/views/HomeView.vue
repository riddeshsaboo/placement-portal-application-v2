<template>
<div>
    <nav class="p-2 bg-body-tertiary">
        <router-link class="navbar-brand" to="/">
            <h3 class="fw-bold">Placement Portal V2</h3>
        </router-link>
    </nav>
    <div class="container">
        <div class="row justify-content-center text-center mt-5">
            <div class="col-lg-8">
                <h1 class="display-4 fw-bold">
                    Placement Portal V2
                </h1>
                <p class="lead mt-3">
                    A centralized platform to manage campus placements, companies, students and recruitment drives efficiently.
                </p>
                <div class="mt-4" v-if="!isLoggedIn">
                    <router-link to="/login" class="btn btn-outline-primary btn-lg m-2">Login</router-link>
                    <router-link to="/register/student" class="btn btn-outline-success btn-lg m-2">Register as Student</router-link>
                    <router-link to="/register/company" class="btn btn-outline-warning btn-lg m-2">Register as Company</router-link>
                </div>
                <div v-else>
                    <router-link to="/login" class="btn btn-outline-primary btn-lg m-2">Dashboard</router-link>
                </div>
            </div>
        </div>
    </div>

    <div class="card shadow m-4">
        <div class="card-body">
            <Bar :data="portalStatisticsChart" :options="chartOptions" />
        </div>
    </div>
        
</div>
</template>

<script>
import axios from 'axios';
import {Chart as ChartJS,CategoryScale,LinearScale,BarElement,Title,Tooltip,Legend} from "chart.js";

import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default {
    data(){
        return {
            isLoggedIn: false,
            loginRole: null,
            total_students:0,
            total_companies:0,
            total_job_postings:0,
            total_applications:0,
            applicants_placed:0
        }
    },
    async mounted(){
        this.checkLoggedIn()
        await this.loadDashboard()
    },

    methods: {
        checkLoggedIn(){
            let role = localStorage.getItem("role")

            if(role == "admin"){
                this.isLoggedIn = true
                this.loginRole = "admin"
            }
            else if(role == "company"){
                this.isLoggedIn = true
                this.loginRole = "company"
            }
            else if(role == "student"){
                this.isLoggedIn = true
                this.loginRole = "student"
            }
            else{
                this.isLoggedIn = false
                this.loginRole = null
            }
        },

        async loadDashboard(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/public/dashboard`)
                this.total_students = response.data.total_students
                this.total_companies = response.data.total_companies
                this.total_job_postings = response.data.total_job_postings
                this.total_applications = response.data.total_applications
                this.applicants_placed = response.data.applicants_placed
            }catch(e){
                console.log(e)
            }

        }
    },
    computed: {
        portalStatisticsChart(){
            return{
                labels:["Students","Companies","Job Postings","Applications","Placed Students"],
                datasets:[{
                    label:"Count",
                    data:[this.total_students,this.total_companies,this.total_job_postings,this.total_applications,this.applicants_placed],
                    backgroundColor:["blue","green","orange","red","purple"],
                    borderRadius:8
                }]
            }
        },

        chartOptions(){
            return{
                responsive:true,
                indexAxis:"y",
                plugins:{
                    legend:{display:false},
                    title:{display:true,text: "Placement Portal Statistics"}
                },
                scales:{
                    x:{beginAtZero:true}
                }
            }
        },
    },
    components: {
        Bar
    }
}
</script>