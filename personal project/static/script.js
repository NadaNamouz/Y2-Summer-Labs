document.addEventListener("DOMContentLoaded", function() {
            fetch('/get_stories')
                .then(response => response.json())
                .then(data => {
                    const container = document.getElementById('stories-container');
                    for (const key in data) {
                        const story = data[key];
                        const storyDiv = document.createElement('div');
                        storyDiv.className = 'story-button';
                        storyDiv.innerHTML = `<h3>${story.title}</h3><p>by ${story.author}</p>`;
                        storyDiv.addEventListener('click', () => showStory(story.title, story.story));
                        container.appendChild(storyDiv);
                    }
                });

            const modal = document.getElementById("story-modal");
            const span = document.getElementsByClassName("close")[0];

            span.onclick = function() {
                modal.style.display = "none";
            }

            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                }
            }
        });

        function showStory(title, content) {
            document.getElementById('story-title').textContent = title;
            document.getElementById('story-content').textContent = content;
            document.getElementById("story-modal").style.display = "block";
        }