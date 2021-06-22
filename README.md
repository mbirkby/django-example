# django-example
A tutorial ecommerce example using Vue, Django and Stripe.

Note:
Most of the stripe has been commented out so payment is currently not functional.  To enable this

1)  Create a strip account
2)  Make a note of the private and public keys
3)  In Checkout.vue submitForm method remove the dummy token
	var result = {
                    token : {id:1},
                } 
4) In Checkout.vue submitForm, uncomment the part that creates the real stripe token
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
5) In Checkout.vue mounted section replace pk_goes_here with your actual public key from stripe in the line
   this.stripe = Stripe('pk_goes_here')


6) In orders/views.py checkout method uncomment the following (which sends the details to stripe)

'''charge = stripe.Charge.create(
                amount=int(paid_amount * 100),#stripe wants it in cents not dollars
                currency='USD',
                description = 'Charge from Djackets',
                source = serializer.validated_data['stripe_token']
            )'''

6) In settings.py replace sk_test_etc with your secret key from stripe in the following line.  Remember this file should be kept as secure
as possible.  Probably the key shouldn't be stored in code but some form of secure repository


STRIPE_SECRET_KEY='sk_test_etc'


	

