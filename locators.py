########## HOME PAGE #######################
campaign_pop_up_xpath = "//div[contains(@class,'campaignModal')]//div[contains(@class,'closeButton')]//button"
famous_destinations_title_xpath = "//div[contains(@class,'chipContainer')]//button"
famous_destinations_link_under_each_title_xpath = "//div[contains(@class,'destinationCardContainer')]//a"
famous_destinations_image_under_each_title_xpath = "//div[contains(@class,'destinationCardContainer')]//img"
ongoing_deals_title_xpath = "//div[contains(@class,'ongoingDeals')]//div[@class='slick-track']//div[contains(@class,'slick-slide')]"
recommended_for_you_titles_xpath = "//span[contains(text(),'Recommended for you')]/ancestor::div[contains(@class,'cardSliderContainer')]//a"

############CART PAGE#######################
empty_cart_text_xpath = "//div[contains(@class,'title') and contains(text(),'Your cart is empty')]"
button_explore_activities_xpath = "//button[contains(@class,'exploreActivitiesBtn')]"
price_per_cart_item_xpath = "//p[contains(@class,'total')]"


########## ACTIVITY PAGE#######################
first_active_date_xpath = "//div[contains(@class,'dateHeader')]//div[contains(@class,'tileContent')]"
button_select_activity_xpath = "//button[text()='Select']"
button_add_activity_to_cart_xpath = "//button[@id='product-add-to-cart-btn']"
button_view_cart_notification_xpath = "//button[contains(text(),'View cart')]"
activity_footer_price_xpath = "//div[contains(@class,'optionPreferenceFooter')]//span[contains(@class,'price')]"