# Replace 'html_content' with the actual HTML content of the page where you want to search.
html_content = """
<div class="offer-main-layout" id="offer-section">
				<input type="hidden" value="12" name="total_offer_hidden" id="total_offer_hidden">				<div class="main-container">
					<div class="">
						<div class="title_top-offers other_seller_header" style="justify-content:left">Other sellers (<span class="pre_total_offer">12</span>)</div>
					</div>

					<!-- testing start-->
					<div class="dynmaic-filter-desk online-seller-section">
						<div class="online-seller-items">
							<div class="online-seller-list">
								<div></div>
								<div class="online-seller-right-section">
									<div class="online-seller-contents">Online sellers</div>
									<div>
										<div class="switch-main-2">
											<div class="toggle" onchange="getSlsOffer(&quot;https://www.g2g.com/checkout/buyNow/offerList?service_id=lgc_service_1&amp;brand_id=lgc_game_19398&amp;fa=lgc_19398_server%3Algc_19398_server_48088%7Clgc_19398_tier%3Algc_19398_tier_42692&amp;sort=lowest_price&amp;include_offline=1&amp;offer_title=-PC--Crucible-Hardcore---Divine-Orb&amp;group=1&amp;load_type=full&amp;offer_sorting=lowest_price&amp;offer_online_status=1&amp;offer_id=58217935&quot;,&quot;full&quot;, &quot;1&quot;, &quot;offer_online_status_mobile&quot;)">
												<input type="checkbox" class="check" id="offer_online_status_mobile" name="offer_online_status" value="0">
												<b class="b switch"></b>
												<b class="b track"></b>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div class="online-seller-items">
							<div class="sort-by-main">
							<div class="toggleSortMobilebtn" onclick="toggleMobileContainer()">
								<div class="res_sort-main">
									<span class="title-sort-content arrowdown-sort" id="mobile_sorting_title">
					Lowest price				</span>
								</div>
							</div>

						</div>
						</div>
					</div>
					<!-- testing snd-->

					<div class="hide-desktop online-seller-section other_seller_header">
						<div class="online-seller-items"></div>
						<div class="online-seller-items">
							<div class="online-seller-list">
								<div></div>
								<div class="online-seller-right-section">
									<div class="online-seller-contents">Online sellers</div>
									<div>
										<div class="switch-main-2">
											<div class="toggle" onchange="getSlsOffer(&quot;https://www.g2g.com/checkout/buyNow/offerList?service_id=lgc_service_1&amp;brand_id=lgc_game_19398&amp;fa=lgc_19398_server%3Algc_19398_server_48088%7Clgc_19398_tier%3Algc_19398_tier_42692&amp;sort=lowest_price&amp;include_offline=1&amp;offer_title=-PC--Crucible-Hardcore---Divine-Orb&amp;group=1&amp;load_type=full&amp;offer_sorting=lowest_price&amp;offer_online_status=1&amp;offer_id=58217935&quot;,&quot;full&quot;, &quot;1&quot;, &quot;offer_online_status&quot;)">
												<input type="checkbox" class="check" id="offer_online_status" name="offer_online_status" value="0">
												<b class="b switch"></b>
												<b class="b track"></b>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>

					<div class="hide-desktop sortby-main-section other_seller_header">
						<div class="title-sortby"><span id="pre_showing_offer"></span></div>
						<div class="sortby-right-section">
							<span class="sortby-items-title">Sort by</span>
							<span class="" onchange="getSlsOffer(&quot;https://www.g2g.com/checkout/buyNow/offerList?service_id=lgc_service_1&amp;brand_id=lgc_game_19398&amp;fa=lgc_19398_server%3Algc_19398_server_48088%7Clgc_19398_tier%3Algc_19398_tier_42692&amp;sort=lowest_price&amp;include_offline=1&amp;offer_title=-PC--Crucible-Hardcore---Divine-Orb&amp;group=1&amp;load_type=full&amp;offer_sorting=lowest_price&amp;offer_online_status=1&amp;offer_id=58217935&quot;,&quot;full&quot;, &quot;1&quot;, &quot;offer_online_status&quot;)">
																	<span class="soryby-items-dynamic">
										<input type="radio" id="sort_1" name="offer_sorting" value="recommended">
										<label for="sort_1" class="sortby-contain-items ">Recommended</label>
									</span>
																	<span class="soryby-items-dynamic">
										<input type="radio" id="sort_2" name="offer_sorting" value="lowest_price" checked="checked">
										<label for="sort_2" class="sortby-contain-items ">Lowest price</label>
									</span>
															</span>
						</div>

					</div>
					<div id="pre_offer_list_loading" style="display: none;">
						<div class="other-seller-offeer_mainbox" id="pre_offer_list_loading_desktop">
							<div class="other_offer-desk-main-box skeleton">
								<div class="flex-1">
									<div class="flex">
										<a rel="noopener noreferrer" class="flex" href="https://www.google.com/">
											<div class="seller-main-container skeleton-round">
												<img class="seller-img-content visibility-hide" src="">
												<div class="seller-indication-main visibility-hide">
													<div class="seller-indicater-counter">10</div>
													<div class="seller_status online"></div>

												</div>
											</div>

											<div class="seller-details skeleton-head">
												<div class="seller__name-detail visibility-hide">test123</div>
												<div class="seller_level-peronal visibility-hide">Personal</div>
											</div>
										</a>


									</div>
								</div>
								<div style="margin-right: 10px;" class="flex-1 align-self skeleton-head">
									<div class="offers-top-tittles visibility-hide">Delivery method</div>
									<div class="flex">
										<a href="">
										</a>
									</div>
								</div>

								<div style="width: 100px;margin-right: 10px;" class="align-self  skeleton-head">
									<div class="offers-top-tittles visibility-hide">Delivery speed</div>
									<!-- <div class="offers-bottom-attributes">
                                            <span>48 hours</span>
                                        </div> -->
								</div>

								<div style="margin-right: 10px;" class="flex-1 align-self skeleton-head">
									<div class="offers-top-tittles visibility-hide">Stock</div>
									<!-- <div class="offers-bottom-attributes">
                                            <span>99,883</span>
                                        </div> -->
								</div>
								<div style="width: 100px;margin-right: 10px;" class=" align-self  skeleton-head">
									<div class="offers-bottom-attributes visibility-hide">
										<div class="offers-top-tittles">Min.purchase</div>
										<!-- <div>
                                                <span>3K</span>
                                            </div> -->
									</div>
								</div>

								<div class="flex-1 align-self skeleton-head">
									<div class="price-other_offers visibility-hide">
										<span class="offer-price-amount">0.000005</span>
										<!-- <span class="offers_amount-currency-regional">MYR / Gold</span> -->
									</div>
								</div>
							</div>
						</div>
						<div class="other_offer-desk-main-box-responsive skeleton" id="pre_offer_list_loading_mobile">
							<div class="content_main-box">
								<div class="offers_top-section">
									<div class="flex space-betwen skeleton-head">
										<div class="visibility-hide">
											<span class="title-offer-sub offers-method-icons">Min.</span>
											<span class="title-offer-content">3K</span>
										</div>
										<div class="visibility-hide">
											<span class="title-offer-sub">Stock</span>
											<span class="title-offer-content">2,050 Gold</span>
										</div>
									</div>

									<div style="margin-top: 20px;" class="items-offer-section flex skeleton-head">
										<div class="flex flex-1 visibility-hide">
											<a href="#" onclick="return false;"></a>
										</div>
										<div class="content-offer-center__element flex-1 flex-end visibility-hide">
											<div class="flex">
												<div class="content-offer-center__element">
													<svg class="time-icon_v2 offers-method-icons">
														<use xlink:href="#v2-clock"></use>
													</svg>
												</div>
												<div class="content-offer-center__element title-offer-content">2 hours</div>
											</div>
										</div>
									</div>

								</div>

								<div class="offers_bottom-section">

									<div class="flex">
										<div class="flex flex-1">
											<div class="seller-main-container skeleton-round">
												<div class="visibility-hide">
													<img class="seller-img-content" src="">
												</div>
												<div class="seller-indication-main visibility-hide">
													<div class="seller-indicater-counter">10</div>
													<div class="seller_status online"></div>

												</div>
											</div>
											<div class="seller-details skeleton-head">
												<div class="seller__name-detail visibility-hide">test123</div>
												<div class="seller_level-peronal visibility-hide">Personal</div>
											</div>
										</div>

										<div class="flex flex-1 flex-end offer-price-main-sections">
											<div class="skeleton-head">
												<span class="visibility-hide offers-price-total">0.057621</span>
												<span class="visibility-hide offers-price-total-currency">MYR</span>
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div id="pre_checkout_sls_offer" class="hide" style="display: block;">
						    <div class="">
    <div class="other-seller-offeer_mainbox">
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58217935" onmouseover="this.style.cursor='pointer'" style="cursor: pointer;">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/sadrel">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/4385283_1679105067765.jpg?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">sadrel</div>
                                <div class="seller_level-peronal">Level 106</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>30</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>13</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.302559</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="65163858" onmouseover="this.style.cursor='pointer'" style="cursor: pointer;">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/IGMoney">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/1000826499_1685970586483.png">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">IGMoney</div>
                                <div class="seller_level-peronal">Level 103</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>5,385</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>15</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.303304</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58358398" onmouseover="this.style.cursor='pointer'" style="cursor: pointer;">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/Bigboy69">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/6492665_1679052309869.png?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">Bigboy69</div>
                                <div class="seller_level-peronal">Level 124</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>536</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>10</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.419</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58074862" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/HellenWong">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/875683_1679051364447.png">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">HellenWong</div>
                                <div class="seller_level-peronal">Level 163</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>8,065,798</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>12</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.446856</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58244171" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/Player">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/473982_1679103468783.png?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">Player</div>
                                <div class="seller_level-peronal">Level 157</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>9,913,864</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>20</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.446856</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58314206" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/MeNimalism">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7222043_1679045226799.jpg?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">MeNimalism</div>
                                <div class="seller_level-peronal">Level 115</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>278</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>30</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.454024</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58280702" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/Dartexx">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/742506_1679051364617.png?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">Dartexx</div>
                                <div class="seller_level-peronal">Level 142</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1,461,218</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>20</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.465475</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="62394927" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/CoreGamers">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/5714185_1679052310167.jpg?">
                                                                        <div class="seller_status "></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">CoreGamers</div>
                                <div class="seller_level-peronal">Level 120</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>99,999</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>10</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">0.465475</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58965377" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/Rambomaniac">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7959882_1687816396201.png">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">Rambomaniac</div>
                                <div class="seller_level-peronal">Level 90</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>20</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>2</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">1.94</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58293993" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/BogOdin_EG">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7708410_1679103467757.png?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">BogOdin_EG</div>
                                <div class="seller_level-peronal">Level 133</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>91</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>2</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">3.72</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58075698" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/BestSpeed">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/3415296_1679105068407.jpg">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">BestSpeed</div>
                                <div class="seller_level-peronal">Level 143</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>989</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>1</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">30.93</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box other_offer-div-box" data-oid="58287189" onmouseover="this.style.cursor='pointer'">
                <div class="flex-1 align-self">
                    <div class="flex">
                        <a class="flex prechekout-non-produdct-details" href="/BoostRoom">
                            <div class="seller-main-container g2g-new-seller-icon-offer">
                                                <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/831656_1679064577731.jpg?">
                                                                        <div class="seller_status online"></div>
                            </div>

                            <div class="seller-details m-l-sm ">
                                <div class="seller__name-detail">BoostRoom</div>
                                <div class="seller_level-peronal">Level 151</div>
                            </div>
                        </a>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Delivery method</div>
                    <div class="flex offer__content-lower-items">
                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                        <div>
                                                            Face to face trade                                                        </div>">
                                <div class="offer-region-section flex">
                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                        </svg>
                                                                    </div>
                            </div>
                                            </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles"> Delivery speed</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>1h</span>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="offers-top-tittles">Stock</div>
                    <div class="offers-bottom-attributes offer__content-lower-items">
                        <span>100</span>
                    </div>
                </div>


                <div class="flex-1 align-self">
                    <div class="offers-bottom-attributes">
                        <div class="offers-top-tittles">Min. purchase</div>
                        <div class="offers-bottom-attributes offer__content-lower-items">
                            <span>1</span>
                        </div>
                    </div>
                </div>

                <div class="flex-1 align-self">
                    <div class="price-other_offers">
                        <span class="offer-price-amount">55</span>
                        <span class="offers_amount-currency-regional">EUR / Unit</span>
                    </div>
                </div>
            </div>
            </div>
    </div>

    <div class="offer-content-list-responsive">
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58217935" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">13 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">30 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/sadrel">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/4385283_1679105067765.jpg?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">sadrel</div>
                                            <div class="seller_level-peronal">Level 106</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.302559</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="65163858" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">15 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">5,385 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/IGMoney">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/1000826499_1685970586483.png">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">IGMoney</div>
                                            <div class="seller_level-peronal">Level 103</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.303304</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58358398" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">10 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">536 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/Bigboy69">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/6492665_1679052309869.png?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">Bigboy69</div>
                                            <div class="seller_level-peronal">Level 124</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.419</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58074862" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">12 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">8,065,798 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/HellenWong">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/875683_1679051364447.png">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">HellenWong</div>
                                            <div class="seller_level-peronal">Level 163</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.446856</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58244171" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">20 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">9,913,864 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/Player">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/473982_1679103468783.png?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">Player</div>
                                            <div class="seller_level-peronal">Level 157</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.446856</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58314206" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">30 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">278 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/MeNimalism">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7222043_1679045226799.jpg?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">MeNimalism</div>
                                            <div class="seller_level-peronal">Level 115</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.454024</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58280702" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">20 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">1,461,218 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/Dartexx">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/742506_1679051364617.png?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">Dartexx</div>
                                            <div class="seller_level-peronal">Level 142</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.465475</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="62394927" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">10 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">99,999 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/CoreGamers">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/5714185_1679052310167.jpg?">
                                                </div>
                                                                                <div class="seller_status "></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">CoreGamers</div>
                                            <div class="seller_level-peronal">Level 120</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">0.465475</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58965377" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">2 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">20 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/Rambomaniac">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7959882_1687816396201.png">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">Rambomaniac</div>
                                            <div class="seller_level-peronal">Level 90</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">1.94</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58293993" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">2 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">91 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/BogOdin_EG">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/7708410_1679103467757.png?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">BogOdin_EG</div>
                                            <div class="seller_level-peronal">Level 133</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">3.72</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58075698" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">1 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">989 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/BestSpeed">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/3415296_1679105068407.jpg">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">BestSpeed</div>
                                            <div class="seller_level-peronal">Level 143</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">30.93</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
                    <div class="other_offer-desk-main-box-responsive other_offer-div-box" data-oid="58287189" onmouseover="this.style.cursor='pointer'">
                <div class="content_main-box">
                    <div class="offers_top-section">
                        <div class="flex space-betwen">
                            <div class="flex">
                                <span class="title-offer-sub offers-method-icons">Min.</span>
                                <span class="title-offer-content">1 </span>
                            </div>
                            <div>
                                <span class="title-offer-sub">Stock</span>
                                <span class="title-offer-content">100 </span>
                            </div>
                        </div>

                        <div class="items-offer-section flex">
                            <div class="flex offer-section-category">
                                                                    <div class="tippy prechekout-non-produdct-details" data-tippy-content="
                                                                <div>
                                                                Face to face trade                                                                </div>">
                                        <div class="offer-region-section flex">
                                                                                            <svg class="delivery__mode-icons delivery__mode-people offers-method-icons">
                                                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#people"></use>
                                                </svg>
                                                                                    </div>
                                    </div>
                                                            </div>
                            <div class="flex-1">
                                <div class="content-offer-center__element flex-1 flex-end">
                                    <div class="flex">
                                        <div class="content-offer-center__element">
                                            <svg class="time-icon_v2 offers-method-icons">
                                                <use xlink:href="#v2-clock"></use>
                                            </svg>
                                        </div>
                                        <div class="content-offer-center__element title-offer-content">1h</div>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="offers_bottom-section">

                        <div class="flex">
                            <a class="prechekout-non-produdct-details" href="/BoostRoom">
                                <div class="flex">
                                    <div class="seller-main-container g2g-new-seller-icon-offer">
                                        <div class="flex">
                                                            <img class="seller-img-content" src="https://assets.g2g.com/user/avatar/831656_1679064577731.jpg?">
                                                </div>
                                                                                <div class="seller_status online"></div>
                                    </div>
                                    <div class="flex align-self">
                                        <div class="default-line_height seller-details m-l-sm">
                                            <div class="seller__name-detail seller-name-offer">BoostRoom</div>
                                            <div class="seller_level-peronal">Level 151</div>
                                        </div>
                                    </div>
                                </div>
                            </a>

                            <div class="flex flex-2 flex-end offer-price-main-sections">
                                <div class="default-line_height offer-total-amount-rspv">
                                    <span class="offers-price-total">55</span>
                                    <span class="offers-price-total-currency">EUR / Unit</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            </div>





<script type="text/javascript">
    var link = true;

    jQuery(document).ready(function() {
        $('.other_offer-div-box').on('click', function(e) {
            if (jQuery(e.target.closest(".prechekout-non-produdct-details")).hasClass("prechekout-non-produdct-details")) {
                // console.log('in');
            } else {
                // console.log('out');
                getPreCheckoutDetails(jQuery(this).attr('data-oid'), 'load', 'true');
            }
        });

        var paginationPage = parseInt($('.cdp').attr('actpage'), 10);
        $('.cdp_i').on('click', function() {
            var go = $(this).attr('href').replace('#!', '');
            if (go === '+1') {
                paginationPage++;
            } else if (go === '-1') {
                paginationPage--;
            } else {
                paginationPage = parseInt(go, 10);
            }
            $('.cdp').attr('actpage', paginationPage);
            // console.log(paginationPage);
            // scrollToAnchor("#offer-section");
            // scrollToOtherSellers("#offer-section");
            scrollToAnchorEvent('#offer-section', event, -76);
            getSlsOffer("https://www.g2g.com/checkout/buyNow/offerList?service_id=lgc_service_1&brand_id=lgc_game_19398&fa=lgc_19398_server%3Algc_19398_server_48088%7Clgc_19398_tier%3Algc_19398_tier_42692&sort=lowest_price&include_offline=1&offer_title=-PC--Crucible-Hardcore---Divine-Orb&group=0&load_type=full&offer_sorting=lowest_price&offer_online_status=1", "offer", paginationPage);
        });

        $('body').on('mouseenter', '.tippy', function(e) {
            tippy('body .tippy', {
                touchHold: true,
                hideOnClick: 'mouseenter',
                interactive: true,
                maxWidth: 180,
                placement: 'auto',
                distance: 10,
                followCursor: false,
                arrow: false,
                animateFill: false,
                animation: 'shift-away',
            })
        });
    });
</script>					</div>

				</div>
			</div>
"""
import time, requests, random, csv, os, sys
from bs4 import BeautifulSoup
from datetime import datetime

import sys
sys.path.insert(0, r'C:\Users\Kufu\PythonProjects\Mchecker\modules')
from SocketClient import Schat
import controlPanel
sys.path.remove(r'C:\Users\Kufu\PythonProjects\Mchecker\modules')


def PriceChecker():
    try:

        def process_sellerInfo(sellerInfo):
            stock_str = sellerInfo.find('div', class_='offers-top-tittles', string='Stock').find_next('span').text.strip()
            level_str = sellerInfo.find('div', class_='seller_level-peronal').text
            seller_list = {
                'name': sellerInfo.find('div', class_='seller__name-detail').text,
                'level': int(level_str.replace('Level ', '')),
                #'delivery_method': sellerInfo.find('div', class_='offers-top-tittles', string='Delivery method').find_next('div', class_='tippy').text.strip(),
                #'delivery_speed': sellerInfo.find('div', class_='offers-top-tittles', string=' Delivery speed').find_next('span').text.strip(),
                'stock': int(stock_str.replace(',', '')),
                #'min_purchase': sellerInfo.find('div', class_='offers-top-tittles', string='Min. purchase').find_next('span').text.strip(),
                'price': float(sellerInfo.find('span', class_='offer-price-amount').text)
                #'currency_unit': sellerInfo.find('span', class_='offers_amount-currency-regional').text
            }
            return seller_list
        
        def store_data_to_csv(data):
            current_datetime = datetime.now()
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day
            # Join the folder name and file name to create the complete file path
            folder_name = r"C:\Users\Kufu\PythonProjects\Mchecker\gBot"
            #folder_name = "gBot"
            file_path = os.path.join(folder_name, f'gdata{current_year}.csv')

            # Write data to the CSV file
            with open(file_path, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data)

        dict_range = controlPanel.dict_range
        OldSeller = {}
        for i in dict_range:
            key = i
            OldSeller[key] = {}

        dict_filled = False
        skip = False
        skip_myname = False
        my_name = controlPanel.my_name
        target_name = controlPanel.target_name
        
        

        ### TEST SWITCH
        test_phase = controlPanel.test_phase
        test_number = 1

        while True:

            if test_phase == False:
                sleep_time = random.randint(600, 900) 

                url = controlPanel.gPriceCheckerURL
                response = requests.get(url)
                html_content = response.text

                soup = BeautifulSoup(html_content, 'html.parser')

                pre_checkout_sls_offer_div = soup.find('div', {'id': 'pre_checkout_sls_offer', 'class': 'hide'})
                other_seller_offer_mainboxes = pre_checkout_sls_offer_div.find_all('div', {'class': 'other-seller-offeer_mainbox'})
                other_seller_offer_mainboxes = other_seller_offer_mainboxes[0]


                Seller = {}
                for i in dict_range:
                    try:
                        Seller[i] = process_sellerInfo(other_seller_offer_mainboxes.find_all('div', {'class': 'other_offer-desk-main-box other_offer-div-box'})[i-1])
                        print(f"Seller[{i}]: {Seller[i]}")
                    except IndexError:
                        # Handle the case where the index is out of range
                        print(f"Error: Seller in position {i} doesn't exist.")
                        print(f"Seller number: {i-1}")
                        break


            elif test_phase == True:
                sleep_time = 20

                import json

                print(test_number)

                if test_number == 1:
                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t1.json', 'r') as json_file:
                        dataTest = json.load(json_file)
                if test_number == 2:
                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t2.json', 'r') as json_file:
                        dataTest = json.load(json_file)
                if test_number == 3:
                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t3.json', 'r') as json_file:
                        dataTest = json.load(json_file)
                if test_number == 4:
                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t4.json', 'r') as json_file:
                        dataTest = json.load(json_file)
                if test_number == 5:
                    with open(rf'C:\Users\Kufu\PythonProjects\Mchecker\gBot\t5.json', 'r') as json_file:
                        dataTest = json.load(json_file)
                    test_number = 0
                    

                test_number += 1

                # Extract data into separate dictionaries
                Seller[1] = dataTest['seller1']
                Seller[2] = dataTest['seller2']
                Seller[3] = dataTest['seller3']
                Seller[4] = dataTest['seller4']

                # Print the extracted dictionaries
                print("Seller 1:", Seller[1])
                print("Seller 2:", Seller[2])
                print("Seller 3:", Seller[3])
                print("Seller 4:", Seller[4])


            # Get the current date and time
            current_datetime = datetime.now()

            # Extract the year, month, day, and time
            current_year = current_datetime.year
            current_month = current_datetime.month
            current_day = current_datetime.day
            current_time = current_datetime.time()

            # Format the time as a string (HH:MM:SS)
            current_time_str = current_time.strftime('%H:%M:%S')

            # Print the results
            print("Time:", current_time_str)
            print("Date:", current_day, "-", current_month, "-", current_year)

            # Store the data (date, time, and offer price) in the CSV file
            date_str = f"{current_day} - {current_month} - {current_year}"
            store_data_to_csv([date_str, current_time.strftime('%H:%M:%S'), Seller[1]['price']])


            NewName = Seller[1]['name']
            NewPrice = Seller[1]['price']
            NewStock = Seller[1]['stock']


            if Seller[1]['name'] != my_name and dict_filled == True:
                # checking if seller with lowest price is still with lowest price
                if Seller[1]['name'] != OldSeller[1]['name'] or Seller[1]['price'] != OldSeller[1]['price'] or Seller[1]['stock'] != OldSeller[1]['stock']:
                    skip = False
                    skip_myname = False
                    new_account_skip = False
                    print(skip)
                    print(f"OldSeller[1]['price']: {OldSeller[1]['price']}")
                    print(f"Seller[1]['price']: {Seller[1]['price']}")
                    print(f"OldSeller[1]['stock']: {OldSeller[1]['stock']}")
                    print(f"Seller[1]['stock']: {Seller[1]['stock']}")

                    print(f"NewPrice: {NewPrice}")
                    print(f"OldPrice: {OldPrice}")
                    print(f"NewStock: {NewStock}")
                    print(f"OldStock: {OldStock}")


                    ### check for new account
                    if Seller[1]['level'] < 5:
                        skip = True
                        new_account_skip = True


                    ### price change 
                    if OldPrice > NewPrice and new_account_skip == False:
                        final_price = OldPrice - NewPrice
                        print(f"final price is: {final_price}, old price is: {OldPrice}, price: {NewPrice}")
                        if final_price < 1:
                            final_price_int = int(final_price * 100)
                            if final_price < 0.01:
                                message = (f"$tts {Seller[1]['name']} stole position")
                                #Schat(message)
                                #print(f"### price change  message is: {message}")
                                skip = True
                            elif final_price < 0.99 and final_price > 0.01:
                                if final_price_int == 1:
                                    message = f"$tts {Seller[1]['name']} lowered price by {final_price_int} cent"
                                elif final_price <= 0.99:
                                    message = f"$tts {Seller[1]['name']} lowered price by {final_price_int} cents"
                                #print(message)
                        else:
                            message = f"$tts {Seller[1]['name']} lowered price by {final_price:.2f} Euro"
                        Schat(message)
                        print(f"### price change  message is: {message}")


                    elif OldPrice < NewPrice and new_account_skip == False:
                        final_price = NewPrice - OldPrice
                        final_price_int = int(final_price * 100)
                        if final_price < 0.01:
                            message = f"$tts price slightly got higher"
                        elif final_price < 1 and final_price > 0.01:
                            message = f"$tts price got higher by {final_price_int} cents"
                        elif final_price_int == 1:
                            message = f"$tts price got higher by {final_price_int} cent"
                        else:
                            message = f"$tts price got higher by {final_price:.2f} Euro"
                        Schat(message)
                        print(f"### price change  message is: {message}")

                    ### part of stock sold
                    elif OldPrice == NewPrice:
                        if skip == False:
                            if NewName == OldName and NewPrice == OldPrice and NewStock < OldStock:
                                #print("### part of stock sold Part 1")
                                #if NewPrice == OldPrice:
                                #print("### part of stock sold Part 2")
                                #if NewStock < OldStock:
                                #print("### part of stock sold Part 1-3")
                                message = f"$tts {NewName} sold {OldStock - NewStock} divines"
                                Schat(message)
                                print(message)
                                skip = True
                
                    else:
                        if new_account_skip == False:
                            message = f"$tts {Seller[1]['name']} just matched price"
                            print(message)
                            #Schat(message)
                            skip = True


                    ### if first position seller sold all his stock
                    if skip == False and new_account_skip == False:
                        if Seller[1]['name'] == OldSeller[2]['name'] and Seller[1]['stock'] == OldSeller[2]['stock'] and Seller[1]['price'] == OldSeller[2]['price']:
                            message = f"{OldSeller[1]['name']} sold all {OldSeller[1]['stock']} divines"
                            message = f"pos 1 sold everything or went offline"
                            #Schat(message)
                            print(f"### if first position seller sold all his stock message is: {message}")
                            skip = True


                    ### stock block
                    if skip == False and new_account_skip == False:
                        if int(Seller[1]['stock']) <= 5:
                            message = f"$tts small amount"
                            #Schat(message)
                            print(f"### stock block message is: {message}")
                        elif int(Seller[1]['stock']) > 80:
                            message = f"$tts large quantity"
                            #Schat(message)
                            print(f"### stock block message is: {message}")
                        elif int(Seller[1]['stock']) >= 30:
                            message = f"$tts big stock"
                            #Schat(message)
                            print(f"### stock block message is: {message}")
                    
                    ### my name check block if price was changed
                    if skip == False and new_account_skip == False:
                        for i in range(2, 5):
                            #current_seller = locals().get(f"seller{i}")
                            #current_seller = Seller[i]
                            if Seller[i]['name'] == my_name:
                                #price = float(current_seller['price'])
                                #price = Seller[i]['price']
                                #price1 = Seller[1]['price']
                                final_price = Seller[i]['price'] - Seller[1]['price']
                                if final_price < 1 and final_price > 0.01:
                                    final_price_int = int(final_price * 100)
                                    message = f"$tts Price difference is {final_price_int} cents"
                                elif final_price <= 0.01:
                                    message = f"$tts slight price difference"
                                elif final_price == 0.01:
                                    final_price_int = int(final_price * 100)
                                    message = f"$tts Price difference is {final_price_int} cent"
                                else:
                                    message = f"$tts Price difference is {final_price:.2f} Euro"
                                #Schat(message)
                                print(f"### my name check block message is: {message}")
                                skip_myname = True

                    if skip_myname == False:
                        if my_name != Seller[1]['name'] and my_name != Seller[2]['name'] and my_name != Seller[3]['name'] and my_name != Seller[4]['name']:
                            message = '$tts You are not in the list!'
                            #Schat(message)
                            print(message)

                else:
                    print("Nothing has changed")
                    
            elif Seller[1]['name'] == my_name:
                print(f"{Seller[1]['name']} has the lowest price")

            target_name_trigger  = 0
            target_name_trigger_cell1 = False
            target_name_trigger_cell2 = False

            if dict_filled == True:
                for i in dict_range:
                    if target_name_trigger_cell1 == False:
                        try:
                            if Seller[i]['name'] == target_name:
                                target_price_new = Seller[i]['price']
                                target_name_trigger += 1
                                target_name_trigger_cell1 = True
                                print(f"{target_name} test cell 1: {target_price_new} and {Seller[i]['price']}")
                        except KeyError:
                            print(f"Error: cell 1 Seller in position {i} doesn't exist.")
                            break
                    if target_name_trigger_cell2 == False:
                        try:
                            if OldSeller[i]['name'] == target_name:
                                target_price_old = OldSeller[i]['price']
                                target_name_trigger += 1
                                target_name_trigger_cell2 = True
                                print(f"{target_name} test cell 2: {target_price_old} and {OldSeller[i]['price']}")
                        except KeyError:
                            print(f"Error: cell 2 Seller in position {i} doesn't exist.")
                            break
                    if target_name_trigger == 2:
                        if target_price_new > target_price_old:
                            message = f"$tts {target_name} raised price"
                            print(message)
                            Schat(message)
                            break
                        elif target_price_new < target_price_old:
                            message = f"{target_name} lowered price"
                            print(message)
                            Schat(message)
                            break
                        else:
                            print(f"{target_name} has same price")
                            break
                    else:
                        continue

            

            print(f"skip: {skip}")

            ### Make current iteration as Old dictionary for sellers
            for i in dict_range:
                try:
                    OldSeller[i] = Seller[i]
                    #print(OldSeller[i])
                except KeyError:
                    #print(f"Error: Seller in position {i} doesn't exist.")
                    break
            

            OldName = NewName
            OldPrice = NewPrice
            OldStock = NewStock

            print("")
            dict_filled = True

            time.sleep(sleep_time)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print the traceback to see the error details
        input("PriceChecker got An error. Press Enter to exit...")

#import threading
#PriceChecker = threading.Thread(target=PriceChecker)
#PriceChecker.start()
PriceChecker()