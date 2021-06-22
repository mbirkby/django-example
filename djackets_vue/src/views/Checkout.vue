<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Checkout</h1>
            </div>
            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>  
                            <th>Quantity</th>
                            <th>Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in cart.items" v-bind:key="item.product.id">
                            <td>{{ item.product.name }}</td>
                            <td>{{ item.product.price}}</td>
                            <td>{{ item.quantity }}</td>
                            <td>£{{ getItemTotal(item).toFixed(2)}}</td>
                        </tr>
                    </tbody>
                    <tfoot>
                        <tr>
                            <td colspan="2">Total</td>
                            <td>{{ cartTotalLength }}</td>
                            <td>{{ cartTotalPrice.toFixed(2) }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="column is-12 box">
                <h2 class="subtitle">Shipping Details</h2>

                <p class="has-text-grey mb-4">* All Fields are required</p>
                <div class="columns is-multiline">
                    <div class="column is-6">
                        <div class="field">
                            <label>First name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="first_name">
                            </div>
                        </div>
                        <div class="field">
                            <label>Last name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="last_name">
                            </div>
                        </div>
                        <div class="field">
                            <label>Email*</label>
                            <div class="control">
                                <input type="email" class="input" v-model="email">
                            </div>
                        </div>
                        <div class="field">
                            <label>Phone*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="phone">
                            </div>
                        </div>
                    </div>
                    <div class="column is-6">
                        <div class="field">
                            <label>Address*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="address">
                            </div>
                        </div>
                        <div class="field">
                            <label>Zipcode*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="zipcode">
                            </div>
                        </div>
                        <div class="field">
                            <label>Place*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="place">
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <hr>

                <div id="card-element" class="mb-5"></div>

                <template v-if="cartTotalLength">
                     <hr>
                     <button @click="submitForm" class="button is-dark">Pay with stripe</button>
                </template>
                
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Checkout',
    data() {
        return {
            cart: {
                items:[],
            },

            stripe: {},
            card: {},
            first_name: '',
            last_name:'',
            email: '',
            phone: '',
            address:'',
            zipcode:'',
            place:'',
            errors:[]
        }
    },
    mounted() {
        document.title = 'Checkout | DJackets'

        this.cart = this.$store.state.cart

        if (this.cartTotalLength > 0) {
            this.stripe = Stripe('pk_goes_here')
            const elements = this.stripe.elements();

            this.card = elements.create('card', { hidePostalCode: true})

            this.card.mount('#card-element')
        }
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        submitForm() {
            console.log('submitting form')
            this.errors=[]
            if (this.first_name === '') {
                this.errors.push('The first name field is empty')
            }

            if (this.last_name === '') {
                this.errors.push('The last name field is empty')
            }

            if (this.email === '') {
                this.errors.push('The email field is empty')
            }

            if (this.phone === '') {
                this.errors.push('The phone field is empty')
            }

            if (this.address === '') {
                this.errors.push('The address field is empty')
            }

            if (this.zipcode === '') {
                this.errors.push('The zipcode field is empty')
            }

            if (this.place === '') {
                this.errors.push('The place field is empty')
            }

            if (!this.errors.length) {
                this.$store.commit('setIsLoading', true)

                

                
                
                var result = {
                    token : {id:1},
                }

                

                /*this.stripe.createToken(this.card).then(result => {
                    if (result.error) {
                        this.$store.commit('setIsLoading', false)
                        this.errors.push('Something went wrong with stripe.  Please try again')
                        console.log(result.error.message)
                    }
                    else {
                        this.stripeTokenHandler(result.token)
                    }
                })*/
                
                
                
                this.stripeTokenHandler(result.token)
            }
        },

        async stripeTokenHandler(token){
            const items = []
           
            for (let i = 0; i < this.cart.items.length; i++) {

                const item = this.cart.items[i]
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }
                items.push(obj)
            }

            const data = {
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'address': this.address,
                'zipcode': this.zipcode,
                'place': this.place,
                'phone': this.phone,
                'items': items,
                'stripe_token': token.id
            }

            await axios
                .post('/api/v1/checkout/', data)
                .then(response => {
                    this.$store.commit('clearCart')
                    this.$router.push('/cart/success')
                })
                .catch(error => {
                    this.errors.push('Something went wrong. Please try again')
                    console.log(error)
                })

                this.$store.commit('setIsLoading', false)
        }
    },
    computed : {
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            },0)
        },

        cartTotalPrice(){
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            },0)
        }
    }
}
</script>
