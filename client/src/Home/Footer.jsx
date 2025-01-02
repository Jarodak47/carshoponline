import React from 'react'
import '../styles/footer.css'
import { BsLinkedin, BsGithub } from 'react-icons/bs'
import logo from '../images/logo.png'

const Footer = () => {
    return (
        <div>
            <section id="contact" className="footer_wrapper">
                <div className="container">
                    <div className="row">
                        <div className="col-lg-5 footer_logo mb-4 mb-lg-0">
                            {/* <img decoding="async" src={logo} width={150} /> */}
                            <h3 style={{ color: 'blueviolet' }}>Car Buy</h3>
                            <p className="footer_text" style={{ textAlign: 'justify' }}>Ce projet est une plateforme de gestion d'achat, de réservation et de location de voitures, développée par des étudiants en Licence 3 Génie Logiciel à l'Université de Yaoundé I. 
                                    Il permet aux utilisateurs de parcourir diverses marques de voitures, de consulter des informations détaillées et de réaliser des transactions sécurisées. 
                                    This project is a car buying, booking, and rental management platform developed by third-year Software Engineering students at the University of Yaoundé I. 
                                    It allows users to browse various car brands, view detailed information, and perform secure transactions..</p>
                        </div>
                        <div className="col-lg-4 px-lg-5 mb-4 mb-lg-0">
                            <h3 className="footer_title" style={{ color: 'blueviolet' }}>Contact</h3>
                            <p className="footer_text">
                                <a ></a><br />
                                <a className="footer-address">
                                     <br />Universite de Yaounde I</a>
                            </p>
                        </div>
                        <div className="col-lg-3 mb-4 mb-lg-0">
                            <h3 className="footer_title" style={{ color: 'blueviolet' }}>Social Media</h3>
                            <p>
                                <a href="" className="footer_social_media_icon" style={{ color: 'white' }}><BsLinkedin size={25} /></a>
                                <a href="" className="footer_social_media_icon" style={{ color: 'white' }}><BsGithub size={25} /></a>
                            </p>
                        </div>
                        <div className="col-12 footer_credits text-center">
                            <span>© 2024 <a>Car Buy</a>™. All Rights Reserved.</span>
                        </div>
                    </div>
                </div>
            </section >
        </div >
    )
}

export default Footer
