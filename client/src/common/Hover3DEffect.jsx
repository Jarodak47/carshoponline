import React from 'react';
import { motion } from 'framer-motion';

const Hover3DEffect = ({ children }) => {
  return (
    <motion.div
      whileHover={{
        rotateY: 15,
        rotateX: -15,
        transition: { duration: 0.3 },
      }}
      style={{ perspective: 1000 }}
    >
      {children}
    </motion.div>
  );
};

export default Hover3DEffect;
