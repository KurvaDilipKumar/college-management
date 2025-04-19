const topButton = document.getElementById("backtotopButton");
        const progressCircle = document.getElementById("progressCircle");
        
        window.onscroll = function () {
            let scrollTop = document.documentElement.scrollTop;
            let scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            let scrollPercent = Math.round((scrollTop / scrollHeight) * 100);
            
            if (scrollTop > 100) {
                topButton.style.opacity = "1";
            } else {
                topButton.style.opacity = "0";
            }
            
            progressCircle.style.setProperty('--progress', scrollPercent + '%');
        };

        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: "smooth" });
        }