from flask import render_template, request, redirect, url_for, session, flash, abort, jsonify
from bizng.forms import ContactForm, LoginForm, RegisterForm, ListingForm, SearchForm, ReviewForm, ReportForm
from bizng import app
from bizng.models import db, User, LGA, Business, Category, State, Review, Report
import bcrypt
from bizng.func import send_email
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.sql import func
import secrets

load_dotenv()

MAPS_API_KEY = getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    searchform = SearchForm()
    if request.method == "POST":
        # Redirect to search page with selected filters
        category = searchform.category.data or "all"
        state = searchform.state.data or "all"
        lga = searchform.lga.data or "all"
        return redirect(
            url_for("search", category=category, state=state, lga=lga, sort="asc")
        )

    return render_template("index.html", searchform=searchform)

@app.route("/search")
def search():
    searchform = SearchForm()

    # Populate dropdowns dynamically
    searchform.state.choices += [(state.id, state.name) for state in State.query.all()]
    searchform.lga.choices += [(lga.id, lga.name) for lga in LGA.query.all()]
    searchform.category.choices += [(category.id, category.name) for category in Category.query.all()]

    # Get filter values from the query parameters
    query_text = request.args.get("query", "").strip()
    category_id = request.args.get("category", "all")
    state_id = request.args.get("state", "all")
    lga_id = request.args.get("lga", "all")
    sort_order = request.args.get("sort", "asc")

    # Start building the query
    query = Business.query

    # Apply name filter using LIKE and wildcards
    if query_text:
        query = query.filter(Business.name.ilike(f"%{query_text}%"))

    # Apply category filter
    if category_id != "all":
        query = query.filter_by(category_id=category_id)

    # Apply state filter
    if state_id != "all":
        query = query.filter_by(state_id=state_id)

    # Apply LGA filter
    if lga_id != "all":
        query = query.filter_by(lga_id=lga_id)

    # Apply sorting
    if sort_order == "desc":
        query = query.order_by(Business.name.desc())
    else:
        query = query.order_by(Business.name.asc())

    # Execute the query
    businesses = query.all()

    return render_template(
        "search.html",
        searchform=searchform,
        businesses=businesses,
        selected_query=query_text,
        selected_category=category_id,
        selected_state=state_id,
        selected_lga=lga_id,
        sort_order=sort_order,
    )

@app.route("/contact", methods=["GET", "POST"])
def contact():
    contactform = ContactForm()
    if request.method == "POST":
        if contactform.validate_on_submit():
            name = contactform.name.data  
            email = contactform.email.data
            subject = contactform.subject.data
            message = contactform.message.data   
            if send_email(email, name, subject, message):
                flash("Email sent successfully!")
                return render_template("contact.html", contactform=contactform)
            else:
                flash("An unexpected error has occurred. please try again")
                return render_template("contact.html", contactform=contactform)
            
    return render_template("contact.html", contactform=contactform)

@app.route("/login", methods=["GET", "POST"])
def login():
    loginform = LoginForm()
    regform = RegisterForm()
    
    if request.method == "POST":
        action = request.form["action"]
        
        if action == "login":
                if loginform.validate_on_submit():
                    email = loginform.email.data
                    password = loginform.password.data
                
                    if email == "admin@mail.com" and password == "adminpassword":
                        session["admin"] = True
                        session["LoggedIn"] = True
                        return redirect(url_for("profile"))
            
                user = db.session.query(User).filter(User.email == email).first()     
                if user:
                    stored_password = user.password
                    check = bcrypt.checkpw(password.encode(), stored_password.encode())
                    if check:
                        session["LoggedIn"] = True
                        session["id"] = user.id
                        return redirect(url_for("profile"))
                    else:
                        flash("Incorrect Password")
                        return redirect(url_for("login"))
                else:
                    flash("Email is invalid")
                    return redirect(url_for("login"))
                
        elif action == "register":
            
            if regform.validate_on_submit():
                print("validate")
                firstname = regform.firstname.data
                lastname = regform.lastname.data
                email = regform.email.data
                password = regform.password.data
                
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                
                user = User(first_name=firstname, last_name=lastname, email = email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                
                session["LoggedIn"] = True
                session["id"] = user.id
            
                return redirect(url_for("profile"))
            else:
                flash("An unexpected error has occured")            
                return render_template("logreg.html", loginform=loginform, regform=regform)    
    return render_template("logreg.html", loginform=loginform, regform=regform)

@app.route("/register", methods=["GET", "POST"])
def register():
    if "LoggedIn" in session:
        listingform = ListingForm()
        
        # If form is submitted, update LGA choices based on selected state
        if request.method == "POST":
            state_id = request.form.get('state')
            if state_id:
                listingform.set_lga_choices(state_id)
                
        if request.method == "POST":
            if listingform.validate_on_submit():
                name = listingform.name.data
                email = listingform.email.data
                category_id = listingform.category.data
                phone = listingform.phoneno.data
                website = listingform.website.data
                address = listingform.address.data
                description = listingform.description.data
                latitude = listingform.latitude.data
                longitude = listingform.longitude.data
                state_id = listingform.state.data
                lga_id = listingform.lga.data

                if listingform.businessimg.data:
                    image = listingform.businessimg.data
                    filename = image.filename
                    generated_filename = secrets.token_urlsafe()
                    file_extension = filename.split(".")[-1]
                    new_filename = generated_filename + "." + file_extension
                    image.save("bizng/static/businessimg/"+new_filename)
                    
                owner_id = session.get("id")
                if not owner_id:
                    flash("You must be logged in to create a business listing.")
                    return redirect(url_for("login"))
                
                new_business = Business(
                    name=name,
                    description=description,
                    phoneno=phone,
                    email=email,
                    img=new_filename,
                    website=website,
                    address=address,
                    longitude=longitude,
                    latitude=latitude,
                    state_id=state_id,
                    category_id=category_id,
                    owner_id=owner_id,
                    lga_id=lga_id,
                )

                db.session.add(new_business)
                db.session.commit()
                
                return redirect(url_for("listing", business_id=new_business.id))
            else:
                for field, errors in listingform.errors.items():
                    for error in errors:
                        flash(f"{field.capitalize()}: {error}", "danger")

        return render_template("listing.html", api_key=MAPS_API_KEY, listingform=listingform)
    return redirect(url_for("login"))

@app.route("/search/business/<int:business_id>", methods=["GET", "POST"])
def listing(business_id):
    
    reviewform = ReviewForm()
    reportform = ReportForm()
    business = Business.query.get_or_404(business_id)

    if business is None:
        flash("Business not found")
        return redirect(url_for('search'))
            
    if request.method == "POST":
        action = request.form.get("action")
        if action == "review" and reviewform.validate_on_submit():
        # Save the review
            review = Review(
                name = reviewform.name.data,
                business_id=business_id,
                comment=reviewform.comment.data
            )
            db.session.add(review)
            db.session.commit()
            flash("Review submitted successfully!", "success")
            return render_template("bpage.html", business=business, api_key=MAPS_API_KEY, reviewform=reviewform, reportform=reportform)
        
        elif action == "report" and reportform.validate_on_submit():
            report_type = reportform.report_type.data
            report_id = reportform.report_id.data
            reason = reportform.reason.data
            details = reportform.details.data

            new_report = Report(
                report_type=report_type,
                report_reason=reason,
                report_details=details,
                business_id=report_id if report_type == "business" else None,
                review_id=report_id if report_type == "review" else None,
            )
            db.session.add(new_report)
            db.session.commit()

            flash("Your report has been submitted successfully.", "success")
            return render_template("bpage.html", business=business, api_key=MAPS_API_KEY, reviewform=reviewform, reportform=reportform)

        # If validation fails, re-render the page with the form errors
        flash("There was an error submitting your report. Please try again.", "danger")
        return render_template("bpage.html", business=business, api_key=MAPS_API_KEY, reviewform=reviewform, reportform=reportform)
            
        business.maps_url = f"https://www.google.com/maps?q={business.latitude},{business.longitude}"
        
    return render_template("bpage.html", business=business, api_key=MAPS_API_KEY, reviewform=reviewform, reportform=reportform)

@app.route("/profile")
def profile():
    if "LoggedIn" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
    
    if "admin" in session:
        return redirect("/admin")
        
    user_id = session.get("id")
    user = User.query.get_or_404(user_id)
    
    # Get user's businesses with their reviews
    businesses = Business.query.filter_by(owner_id=user_id).all()
    
    # Calculate statistics
    total_reviews = sum(len(business.reviews) for business in businesses)
    
    return render_template(
        "profile.html",
        user=user,
        businesses=businesses,
        total_reviews=total_reviews,
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(error):
    title = "Page Not Found"
    content = "The page you are looking for might have been removed or is temporarily unavailable."
    return render_template("error.html", error=404, title=title, content=content), 404

@app.errorhandler(500)
def server_error(error):
    title = "Internal Server Error"
    content = "Something unexpected has occurred. Please try again later"
    return render_template("error.html", error=500, title=title, content=content), 500

@app.route("/admin")
def admin():
    if "admin" not in session:
        abort(404)
        
    # Get statistics
    total_businesses = Business.query.count()
    total_users = User.query.count()
    total_reviews = Review.query.count()
    total_reports = Report.query.count()  # Add total reports
    
    # Get latest businesses
    latest_businesses = Business.query.order_by(Business.date_added.desc()).limit(5).all()
    
    # Get latest users
    latest_users = User.query.order_by(User.date_registered.desc()).limit(5).all()
    
    # Get latest reviews
    latest_reviews = Review.query.order_by(Review.date_reviewed.desc()).limit(5).all()
    
    pending_reports = Report.query.order_by(Report.date_reported.desc()).limit(5).all()
    
    return render_template(
        "admin.html",
        total_businesses=total_businesses,
        total_users=total_users,
        total_reviews=total_reviews,
        total_reports=total_reports,  # Pass total reports to the template
        latest_businesses=latest_businesses,
        latest_users=latest_users,
        latest_reviews=latest_reviews, 
        pending_reports=pending_reports
    )

@app.route("/admin/businesses")
def admin_businesses():
    if "admin" not in session:
        abort(404)
        
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    businesses = Business.query.order_by(Business.date_added.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    
    return render_template("admin_businesses.html", businesses=businesses)

@app.route("/admin/users")
def admin_users():
    if "admin" not in session:
        abort(404)
        
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    users = User.query.order_by(User.date_registered.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template("admin_users.html", users=users)

@app.route("/admin/reviews")
def admin_reviews():
    if "admin" not in session:
        abort(404)
    reviews = Review.query.all()
    return render_template('admin_reviews.html', reviews=reviews)

@app.route("/admin/ban_user/<int:user_id>", methods=["POST"])
def ban_user(user_id):
    if "admin" not in session:
        return jsonify({"success": False, "message": "Unauthorized"})
        
    try:
        user = User.query.get_or_404(user_id)
        
        
        # Delete all businesses owned by this user
        businesses = Business.query.filter_by(owner_id=user_id).all()
        for business in businesses:
            # Delete reviews for each business
            Review.query.filter_by(business_id=business.id).delete()
            # Delete the business
            db.session.delete(business)
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "User banned successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error banning user: {str(e)}"
        })

@app.route("/admin/delete_review/<int:review_id>", methods=["POST"])
def delete_review(review_id):
    if "admin" not in session:
        abort(404)
    try:
        review = Review.query.get_or_404(review_id)
        business = Business.query.get(review.business_id)
        
        # Update business rating
        total_reviews = Review.query.filter_by(business_id=review.business_id).count()
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Review deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route("/admin/delete_business/<int:business_id>", methods=["POST"])
def admin_delete_business(business_id):
    if "admin" not in session:
        return jsonify({"success": False, "message": "Unauthorized"})
        
    try:
        business = Business.query.get_or_404(business_id)
        
        # Delete associated reviews first
        Review.query.filter_by(business_id=business_id).delete()
        
        # Delete the business
        db.session.delete(business)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Business deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error deleting business: {str(e)}"
        })

@app.route("/get_lgas/<int:state_id>")
def get_lgas(state_id):
    lgas = LGA.query.filter_by(state_id=state_id).all()
    return jsonify({"lgas": [{"id": lga.id, "name": lga.name} for lga in lgas]})

@app.route("/filter_businesses")
def filter_businesses():
    category_id = request.args.get("category", "all")
    state_id = request.args.get("state", "all")
    lga_id = request.args.get("lga", "all")
    sort_order = request.args.get("sort", "asc")

    query = Business.query

    if category_id != "all":
        query = query.filter_by(category_id=category_id)
    if state_id != "all":
        query = query.filter_by(state_id=state_id)
    if lga_id != "all":
        query = query.filter_by(lga_id=lga_id)

    if sort_order == "desc":
        query = query.order_by(Business.name.desc())
    else:
        query = query.order_by(Business.name.asc())

    businesses = query.all()
    return jsonify([
        {
            "id": business.id,
            "name": business.name,
            "category": business.category.name,
            "state": business.state.name,
            "lga": business.lga.name,
            "phone": business.phoneno,
        }
        for business in businesses
    ])

@app.route("/delete_business/<int:business_id>", methods=["POST"])
def delete_business(business_id):
    if "LoggedIn" not in session:
        return jsonify({"success": False, "message": "Please log in first"})
        
    try:
        business = Business.query.get_or_404(business_id)
        
        # Check if user owns the business or is admin
        if business.owner_id != session.get("id") :
            return jsonify({"success": False, "message": "Unauthorized to delete this business"})
        
        # Delete associated reviews first
        Review.query.filter_by(business_id=business_id).delete()
        
        # Delete the business
        db.session.delete(business)
        db.session.commit()
        
        return jsonify({
            "success": True, 
            "message": "Business deleted successfully"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error deleting business: {str(e)}"
        })

@app.route("/edit_business/<int:business_id>", methods=["GET", "POST"])
def edit_business(business_id):
    if "LoggedIn" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
        
    business = Business.query.get_or_404(business_id)
    
    # Check if user owns the business
    if business.owner_id != session.get("id") and "admin" not in session:
        flash("Unauthorized to edit this business")
        return redirect(url_for("profile"))
    
    form = ListingForm(obj=business)
    
    # Populate state, LGA, and category choices
    form.state.choices = [(state.id, state.name) for state in State.query.all()]
    form.lga.choices = [(lga.id, lga.name) for lga in LGA.query.filter_by(state_id=business.state_id).all()]
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    
    if request.method == "POST" and form.validate_on_submit():
        try:
            business.name = form.name.data
            business.email = form.email.data
            business.phoneno = form.phoneno.data
            business.description = form.description.data
            business.website = form.website.data
            business.address = form.address.data
            business.latitude = form.latitude.data
            business.longitude = form.longitude.data
            business.state_id = form.state.data
            business.category_id = form.category.data
            business.lga_id = form.lga.data
            
            # Handle image upload
            if form.businessimg.data:
                image = form.businessimg.data
                filename = image.filename
                generated_filename = secrets.token_urlsafe()
                file_extension = filename.split(".")[-1]
                new_filename = generated_filename + "." + file_extension
                image.save(f"bizng/static/businessimg/{new_filename}")
                business.img = new_filename
            
            db.session.commit()
            return redirect(url_for("listing", business_id=business_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating business: {str(e)}")
    
    return render_template("edit_business.html", form=form, business=business, api_key=MAPS_API_KEY)

@app.route("/add_review/<int:business_id>", methods=["POST"])
def add_review(business_id):
        
    try:
        business = Business.query.get_or_404(business_id)
        
        # Check if user owns the business
        if business.owner_id == session.get("id"):
            return jsonify({"success": False, "message": "You cannot review your own business"})
            
        # Check if user has already reviewed this business
        existing_review = Review.query.filter_by(
            business_id=business_id,
            customer_id=session.get("id")
        ).first()
        
        if existing_review:
            return jsonify({"success": False, "message": "You have already reviewed this business"})
        
        comment = request.form.get("comment")
        
        if not comment:
            return jsonify({"success": False, "message": "Comment is required"})
        
        review = Review(
            comment=comment,
            business_id=business_id,
            customer_id=session.get("id")
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Review added successfully",
            "review": {
                "rating": review.rating,
                "comment": review.comment,
                "customer_name": f"{review.customer.first_name} {review.customer.last_name}",
                "date": review.date_reviewed.strftime('%B %d, %Y')
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error adding review: {str(e)}"
        })

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "LoggedIn" not in session:
        flash("Please log in first.")
        return redirect(url_for("login"))
        
    user = User.query.get_or_404(session.get("id"))
    form = RegisterForm()
    
    if request.method == "POST":
        try:
            # Get form data
            first_name = form.firstname.data
            last_name = form.lastname.data
            email = form.email.data  
            
            if form.change_password.data:
                hashed_password = bcrypt.hashpw(form.change_password.data.encode(), bcrypt.gensalt())
                user.password = hashed_password
            
            if form.dp.data:
                image = form.dp.data
                filename = image.filename
                generated_filename = secrets.token_urlsafe()
                file_extension = filename.split(".")[-1]
                new_filename = generated_filename + "." + file_extension
                image.save(f"bizng/static/userimg/{new_filename}")
                user.dp = new_filename
            
            # Update other fields
            user.first_name = first_name
            user.last_name = last_name
            
            
            # Check if email is being changed and not already taken
            if email != user.email:
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash("Email already in use")
                    return redirect(url_for("edit_profile"))
                user.email = email
            
            db.session.commit()
            flash("Profile updated successfully!")
            return redirect(url_for("profile"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}")
            return redirect(url_for("edit_profile"))
        
    form.firstname.data = user.first_name
    form.lastname.data = user.last_name
    form.email.data = user.email
    
    return render_template("edit_profile.html", user=user, form=form)

@app.route("/delete_profile", methods=["POST"])
def delete_profile():
    if "LoggedIn" not in session:
        return jsonify({"success": False, "message": "Please log in first"})
        
    try:
        user_id = session.get("id")
        user = User.query.get_or_404(user_id)
        
        
        # Delete all businesses owned by this user
        businesses = Business.query.filter_by(owner_id=user_id).all()
        for business in businesses:
            # Delete reviews for each business
            Review.query.filter_by(business_id=business.id).delete()
            # Delete the business
            db.session.delete(business)
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Clear session
        session.clear()
        
        return jsonify({
            "success": True,
            "message": "Profile deleted successfully"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"Error deleting profile: {str(e)}"
        })
        
@app.route("/admin/reports")
def admin_reports():
    if "admin" not in session:
        abort(404)

    # Fetch all reports
    reports = Report.query.order_by(Report.date_reported.desc()).all()

    return render_template("admin_reports.html", reports=reports)

@app.route("/admin/reports/delete/<int:report_id>", methods=["DELETE"])
def delete_report(report_id):
    if "admin" not in session:
        abort(404)

    try:
        
        return jsonify({"success": True, "message": "Report deleted successfully."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error deleting report: {str(e)}"})