const items1 = document.querySelectorAll('.delete-button')
        for (let i = 0; i < items1.length; i++) {
            const item = items1[i]
            item.onclick = function(e) {
                console.log('click event: ', e)
                const product_id = e.target.dataset['id'];
                fetch('/product/'+product_id+'/delete-product', {
                    method: 'DELETE'
                }).then(function() {
                    const item = e.target.parentElement
                    item.remove()
                });
            }
        }