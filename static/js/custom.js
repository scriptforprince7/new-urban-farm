$(document).ready(function () {
  $(".add-to-cart-btn").on("click", function () {
    let this_val = $(this);
    let index = this_val.attr("data-index");
    let quantity = $(".product-quantity-" + index).val();
    let product_title = $(".product-title-" + index).val();
    let product_id = $(".product-id-" + index).val();
    let product_price = $(".product-price-" + index).val();
    let product_price_wo_gst = $(".product-price-wo-gst-" + index).val();
    let gst_rate = $(".gst_rate-" + index).val();
    let maximum_order_qty = $(".maximum_order_qty-" + index).val();
    let gst_applied = $(".gst-applied-" + index).val();
    let product_sku = $(".product-sku-" + index).val();
    let product_image = $(".product-image-" + index).val();
    let selected_variant_type_id = $("#variant-id-hidden-" + index).val(); // Updated line
    let selected_variation_type_id = $("#variation-id-hidden").val(); // Updated line
    let max_order_qty = parseInt($(".product-quantity-" + index).attr('max')); // Get the maximum order quantity

    console.log("Quantity:", quantity);
    console.log("Title:", product_title);
    console.log("Price:", product_price);
    console.log("Price Without Gst:", product_price_wo_gst);
    console.log("gst_rate:", gst_rate);
    console.log("GST Applied:", gst_applied);
    console.log("Max Order Qty:", maximum_order_qty)
    console.log("ID:", product_id);
    console.log("Image:", product_image);
    console.log("Sku:", product_sku);
    console.log("Variant ID:", selected_variant_type_id);
    console.log("Variation ID:", selected_variation_type_id);
    console.log("Index:", index);
    console.log("Current Element:", this_val);

    // Check if the quantity exceeds the maximum order quantity
    if (parseInt(quantity) > max_order_qty) {
      Swal.fire({
        position: "top-end",
        icon: "warning",
        title: "Maximum order quantity exceeded",
        showConfirmButton: false,
        timer: 1500,
      });
      return; // Prevent further execution
    }

    $.ajax({
      url: "/add-to-cart",
      data: {
        id: product_id,
        image: product_image,
        qty: quantity,
        title: product_title,
        price: product_price,
        price_wo_gst: product_price_wo_gst,
        gst_rate: gst_rate,
        gst_applied: gst_applied,
        maximum_order_qty: maximum_order_qty,
        sku: product_sku,
        variant_id: selected_variant_type_id, // Updated line
        variation_id: selected_variation_type_id, // Updated line
      },
      dataType: "json",
      beforeSend: function () {
        console.log("Adding Product to the cart...");
      },
      success: function (response) {
        if (response.already_in_cart) {
          // Show alert that product is already in the cart
          Swal.fire({
            position: "top-end",
            icon: "info",
            title: "Product is already in your cart",
            showConfirmButton: false,
            timer: 1500,
          });
        } else {
          // Show success alert and update cart
          this_val.html("✓");
          console.log("Added Product to cart!");
          updateCartItemsList(response.data);
          $(".cart-items-count").text(response.totalcartitems);

          Swal.fire({
            position: "top-end",
            icon: "success",
            title: "Product has been added to your cart",
            showConfirmButton: false,
            timer: 1500,
          });
        }
      },
    });
  });
});


function cleanTitle(title) {
  // Use a regex to remove the variant part (e.g., "- (50Pcs)")
  return title.replace(/\s*-\s*\(.*?\)$/, "");
}

function generateProductUrl(baseUrl, title) {
  var cleanedTitle = cleanTitle(title);
  // Encode the cleaned title to be URL-safe
  var encodedTitle = encodeURIComponent(cleanedTitle);
  return `${baseUrl}${encodedTitle}/`;
}

function updateCartItemsList(cartData) {
  var cartItemsList = $(".cart-drawer-items-list");
  cartItemsList.empty(); // Clear existing items

  var subtotalAmount = 0; // Initialize subtotal amount

  var baseUrl = "https://beta.urbanfarm.store/product/"; // Change to your actual base URL

  // Iterate over cart items and append them to the list
  $.each(cartData, function (productId, item) {
      var productUrl = generateProductUrl(baseUrl, item.title);
      var itemHtml = `
          <div class="cart-drawer-item d-flex position-relative">
              <div class="position-relative">
                  <img loading="lazy" class="cart-drawer-item__img" src="${item.image}" alt="${item.title}" />
              </div>
              <div class="cart-drawer-item__info flex-grow-1">
                  <a href="${productUrl}">
                      <h6 class="cart-drawer-item__title fw-normal">${item.title}</h6>
                  </a>
                  <p class="cart-drawer-item__option text-secondary">Sku ID: ${item.sku}</p>
                  <div class="d-flex align-items-center justify-content-between mt-1">
                      <div class="qty-control position-relative">
                          <input type="number" name="quantity" value="${item.qty}" min="1"
                              class="qty-control__number border-0 text-center update-product product-qty-${productId}" data-product="${productId}" />
                          <div class="qty-control__reduce text-start update-product" data-product="${productId}">-</div>
                          <div class="qty-control__increase text-end update-product" data-product="${productId}">+</div>
                      </div>
                      <span class="cart-drawer-item__price money price">₹ ${item.price}</span>
                  </div>
              </div>
              <button class="btn-close-xs position-absolute top-0 end-0 remove-cart delete-product" data-product="${productId}"></button>
          </div>
          <hr class="cart-drawer-divider" />`; // Add HR after each item
      cartItemsList.append(itemHtml);

      // Add item price to subtotal
      subtotalAmount += parseFloat(item.price) * item.qty;
  });

  // Update subtotal amount
  $(".cart-subtotal").text(`₹ ${subtotalAmount.toFixed(2)}`);

  // Attach event listeners for quantity increase and decrease buttons
  cartItemsList.on("click", ".qty-control__increase", function () {
      var productId = $(this).data("product");
      updateQuantity(productId, 1);
  });

  cartItemsList.on("click", ".qty-control__reduce", function () {
      var productId = $(this).data("product");
      updateQuantity(productId, -1);
  });

  // Function to handle quantity update
  function updateQuantity(productId, change) {
      var inputField = $(".product-qty-" + productId);
      var newQty = parseInt(inputField.val()) + change;

      if (newQty >= 1) {
          inputField.val(newQty);

          $.ajax({
      url: "/update-cart",
      data: {
        id: productId,
        qty: newQty,
        refresh_page: true,
      },
      dataType: "json",
      success: function (response) {
        $(".cart-items-count").text(response.totalcartitems);
        $("#cart-list").html(response.data);

        if (response.refresh_page) {
          // Refresh the page
          window.location.reload();
        }
      },
    });
      }
  }
}




$(document).ready(function () {
  // Event delegation for delete buttons
  $(document).on("click", ".delete-product", function () {
    let product_id = $(this).attr("data-product");
    let this_val = $(this);

    console.log("Product ID:", product_id);

    // Display SweetAlert confirmation dialog
    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        // User confirmed the deletion, proceed with AJAX request
        $.ajax({
          url: "/delete-from-cart",
          data: {
            id: product_id,
            refresh_page: true, // Add a parameter to indicate page refresh
          },
          dataType: "json",
          beforeSend: function () {
            this_val.hide();
          },
          success: function (response) {
            this_val.show();
            $(".cart-items-count").text(response.totalcartitems);
            $("#cart-list").html(response.data);

            // Set a flag in local storage before refreshing the page
            localStorage.setItem("productDeleted", "true");

            // Refresh the page
            window.location.reload();
          },
        });
      }
    });
  });

  // Check if the productDeleted flag is set in local storage
  if (localStorage.getItem("productDeleted") === "true") {
    // Show the alert that the product is deleted
    Swal.fire({
      title: "Deleted!",
      text: "Product has been deleted.",
      icon: "success",
      timer: 2000, // 1 second
      confirmButtonText: "OK",
    });

    // Remove the flag from local storage
    localStorage.removeItem("productDeleted");
  }
});

$(document).ready(function () {
  $(".update-product").on("click", function () {
      let product_id = $(this).attr("data-product");
      let this_val = $(this);
      let product_quantity = $(".product-qty-" + product_id).val();
      let max_order_qty = parseInt($(".product-qty-" + product_id).attr('max'));

      console.log("Product ID:", product_id);
      console.log("Product Qty:", product_quantity);

      // Check if the quantity exceeds the maximum order quantity
      if (parseInt(product_quantity) > max_order_qty) {
          Swal.fire({
              position: "top-end",
              icon: "warning",
              title: "Maximum order quantity exceeded",
              showConfirmButton: false,
              timer: 1500,
          });
          return; // Prevent further execution
      }

      $.ajax({
          url: "/update-cart",
          data: {
              id: product_id,
              qty: product_quantity,
              refresh_page: true,
          },
          dataType: "json",
          beforeSend: function () {
              this_val.hide();
          },
          success: function (response) {
              this_val.show();
              $(".cart-items-count").text(response.totalcartitems);
              $("#cart-list").html(response.data);

              if (response.refresh_page) {
                  localStorage.setItem('openCartDrawer', 'true');
                  // Refresh the page
                  window.location.reload();
              }
          },
      });
  });

  if (localStorage.getItem('openCartDrawer') === 'true') {
      // Open the cart drawer
      $("#cartDrawer").addClass('aside_visible');
      // Remove the flag so it doesn't open on subsequent page loads
      localStorage.removeItem('openCartDrawer');
  }
});
