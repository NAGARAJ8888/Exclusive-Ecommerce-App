  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".heart-icon").forEach((icon) => {
      icon.addEventListener("click", function () {
        const productId = this.dataset.productId;
        const img = this;

        fetch("{% url 'toggle_wishlist' %}", {
          method: "POST",
          headers: {
            "X-CSRFToken": "{{ csrf_token }}",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: `product_id=${productId}`,
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "added") {
              img.src = "{% static 'red_heart.png' %}";
            } else if (data.status === "removed") {
              img.src = "{% static 'white_heart.png' %}";
            }
          });
      });
    });
  });



  document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.cookie.match(/csrftoken=([\w-]+)/)?.[1];

    document.querySelectorAll(".add-to-cart-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        const productId = btn.getAttribute("data-product-id");

        fetch(`/add-to-cart/${productId}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status === "success") {
              alert("Product added to cart!");
              // optionally update cart count here
            }
          });
      });
    });
  });



  const scroller = document.getElementById("productScroller");
  const scrollLeftBtn = document.getElementById("scrollLeft");
  const scrollRightBtn = document.getElementById("scrollRight");

  const scrollAmount = 300; // adjust this value based on your card size

  scrollLeftBtn.addEventListener("click", () => {
    scroller.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  });

  scrollRightBtn.addEventListener("click", () => {
    scroller.scrollBy({ left: scrollAmount, behavior: "smooth" });
  });


  function showToast(message, type = "info") {
    const toast = document.createElement("div");

    // Set Tailwind styles based on type
    let bgColor = "bg-blue-500";
    if (type === "error") bgColor = "bg-red-500";
    if (type === "success") bgColor = "bg-green-500";
    if (type === "warning") bgColor = "bg-yellow-500";

    toast.className = `${bgColor} text-white px-4 py-2 rounded shadow-md animate-slide-in`;
    toast.textContent = message;

    document.getElementById("toast-container").appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
      toast.classList.add("opacity-0");
      setTimeout(() => toast.remove(), 500);
    }, 3000);
  }


  function handleWishlist() {
    const isLoggedIn = {{ request.user.is_authenticated|yesno:"true,false" }}; // Replace with actual login check

    if (!isLoggedIn) {
      showToast('You need to log in to use the wishlist!', 'error');
      return;
    }

    // wishlist logic here
  }


  const now = new Date().getTime();
  const targetDate = now + 3 * 24 * 60 * 60 * 1000; // 3 days in milliseconds

  const countdown = setInterval(() => {
    const currentTime = new Date().getTime();
    const diff = targetDate - currentTime;

    if (diff <= 0) {
      clearInterval(countdown);
      document.getElementById("days").textContent = "00";
      document.getElementById("hours").textContent = "00";
      document.getElementById("minutes").textContent = "00";
      document.getElementById("seconds").textContent = "00";
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    document.getElementById("days").textContent = String(days).padStart(2, "0");
    document.getElementById("hours").textContent = String(hours).padStart(
      2,
      "0"
    );
    document.getElementById("minutes").textContent = String(minutes).padStart(
      2,
      "0"
    );
    document.getElementById("seconds").textContent = String(seconds).padStart(
      2,
      "0"
    );
  }, 1000);


  function scrollToTop() {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }



  const carousel = document.getElementById("carousel");
  const dots = document.querySelectorAll(".dot");
  const totalSlides = dots.length;
  let index = 0;
  let isTransitioning = false;

  function updateDots() {
    dots.forEach((dot, idx) => {
      dot.classList.toggle("bg-red-500", idx === index);
      dot.classList.toggle("bg-gray-500", idx !== index);
    });
  }

  function goToSlide(i) {
    index = i;
    carousel.style.transition = "transform 0.7s ease-in-out";
    carousel.style.transform = `translateX(-${index * 100}%)`;
    updateDots();
  }

  function nextSlide() {
    if (isTransitioning) return;
    isTransitioning = true;
    index++;
    carousel.style.transition = "transform 0.7s ease-in-out";
    carousel.style.transform = `translateX(-${index * 100}%)`;
  }

  carousel.addEventListener("transitionend", () => {
    if (index === totalSlides) {
      carousel.style.transition = "none";
      index = 0;
      carousel.style.transform = `translateX(0)`;
    }
    updateDots();
    setTimeout(() => (isTransitioning = false), 20);
  });

  dots.forEach((dot, idx) => {
    dot.addEventListener("click", () => goToSlide(idx));
  });

  setInterval(nextSlide, 5000);

  updateDots();