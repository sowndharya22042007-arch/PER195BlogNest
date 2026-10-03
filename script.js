let editingId = null;

async function checkAPI() {
    try {
        const response = await fetch("/api/health");
        const data = await response.json();
        document.getElementById("status").textContent = "● API is running";
    } catch (error) {
        document.getElementById("status").textContent = "API connection unavailable";
    }
}

async function loadBlogs() {
    const response = await fetch("/api/blogs");
    const blogs = await response.json();
    const query = document.getElementById("search").value.toLowerCase();
    const list = document.getElementById("blogList");

    const filtered = blogs.filter(blog =>
        `${blog.title} ${blog.content} ${blog.category}`.toLowerCase().includes(query)
    );

    if (!filtered.length) {
        list.innerHTML = '<div class="empty">No blogs found.</div>';
        return;
    }

    list.innerHTML = filtered.map(blog => `
        <article class="blog">
            <h3>${escapeHTML(blog.title)}</h3>
            <span class="badge">${escapeHTML(blog.category)}</span>
            <p>${escapeHTML(blog.content)}</p>
            <div class="blog-actions">
                <button class="secondary" onclick="editBlog(${blog.id})">Edit</button>
                <button class="secondary" onclick="deleteBlog(${blog.id})">Delete</button>
            </div>
        </article>
    `).join("");
}

async function saveBlog() {
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();
    const category = document.getElementById("category").value;

    if (!content) {
        showMessage("Please enter blog content.");
        return;
    }

    const url = editingId ? `/api/blogs/${editingId}` : "/api/blogs";
    const method = editingId ? "PUT" : "POST";

    const response = await fetch(url, {
        method,
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, content, category})
    });
    const data = await response.json();

    if (!response.ok) {
        showMessage(data.error || "Something went wrong.");
        return;
    }

    showMessage(editingId ? "Blog updated successfully." : "Blog created successfully.");
    resetForm();
    loadBlogs();
}

async function getAISuggestion() {
    const title = document.getElementById("title").value.trim();
    const content = document.getElementById("content").value.trim();

    if (!content && !title) {
        showMessage("Enter a title or some content first.");
        return;
    }

    const response = await fetch("/api/ai/suggest", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, content})
    });
    const data = await response.json();

    document.getElementById("title").value = data.suggested_title;
    document.getElementById("category").value = data.suggested_category;
    showMessage(`AI suggestion: ${data.suggested_category}`);
}

async function editBlog(id) {
    const response = await fetch("/api/blogs");
    const blogs = await response.json();
    const blog = blogs.find(item => item.id === id);
    if (!blog) return;

    editingId = id;
    document.getElementById("formTitle").textContent = "Edit Blog";
    document.getElementById("title").value = blog.title;
    document.getElementById("content").value = blog.content;
    document.getElementById("category").value = blog.category;
    window.scrollTo({top: 0, behavior: "smooth"});
}

async function deleteBlog(id) {
    if (!confirm("Delete this blog?")) return;
    await fetch(`/api/blogs/${id}`, {method: "DELETE"});
    loadBlogs();
}

function resetForm() {
    editingId = null;
    document.getElementById("formTitle").textContent = "Create a Blog";
    document.getElementById("title").value = "";
    document.getElementById("content").value = "";
    document.getElementById("category").value = "";
}

function showMessage(text) {
    document.getElementById("message").textContent = text;
}

function escapeHTML(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

checkAPI();
loadBlogs();
